def passive_greedy(actions,agent_actions):
    agent_1_actions=[]
    agent_2_actions=[]
    agent_3_actions=[]
    real_rounds=actions['real_round']
    for i in agent_actions.columns:
        agent_actions[i]=pd.to_numeric(agent_actions[i])
    for i in actions.iloc[:,1:].columns:
        actions[i]=pd.to_numeric(actions[i])
    for i in actions['actions']:
        agent_1_actions.append(float(actions[actions.actions==i]['unit_utility'].values)*float(agent_actions.loc[(agent_actions.index=='agent_1'),i].values))
        agent_2_actions.append(float(actions[actions.actions==i]['unit_utility'].values)*float(agent_actions.loc[(agent_actions.index=='agent_2'),i].values))
        agent_3_actions.append(float(actions[actions.actions==i]['unit_utility'].values)*float(agent_actions.loc[(agent_actions.index=='agent_3'),i].values))
    actions['agent_1']=pd.Series(agent_1_actions)
    actions['agent_2']=pd.Series(agent_2_actions)
    actions['agent_3']=pd.Series(agent_3_actions)
    k=0.01
    first_actions={'agents':['agent_1','agent_2','agent_3'],'actions':['B22','B3','B15']}
    first_actions=pd.DataFrame(first_actions)
    changed_actions=[]
    recent_actions=first_actions.copy()
    e1=[]
    e2=[]
    e3=[]
    u1=[]
    u2=[]
    u3=[]
    e_1=recent_actions.loc[recent_actions.agents=='agent_1','actions'].values[0]

    e_2=recent_actions.loc[recent_actions.agents=='agent_2','actions'].values[0]

    e_3=recent_actions.loc[recent_actions.agents=='agent_3','actions'].values[0]
    beginning_actions=list(first_actions.actions)
    finished_actions=[]
    agent_1_oncul=[]    
    agent_2_oncul=[]
    agent_3_oncul=[]

    for i in list(agent_actions.columns):
        if agent_actions.loc[(agent_actions.index=='agent_1'),i].values==1:
            agent_1_oncul.append(i)
        elif agent_actions.loc[(agent_actions.index=='agent_2'),i].values==1:
            agent_2_oncul.append(i)
        else:
            agent_3_oncul.append(i)
    agent_1_oncul=pd.Series(agent_1_oncul,name='agent_1')
    agent_2_oncul=pd.Series(agent_2_oncul,name='agent_2')
    agent_3_oncul=pd.Series(agent_3_oncul,name='agent_3')
    oncul=pd.concat([agent_1_oncul,agent_2_oncul,agent_3_oncul],axis=1)

    while len(actions)>3:
        
        if len(recent_actions.actions.unique())<3:
            ajans=list(recent_actions.loc[recent_actions.actions.duplicated(),'agents'])
            duplicated_action=recent_actions.loc[recent_actions.actions.duplicated(),'actions'].unique()[0]
            worse_agent=agent_actions[agent_actions.index.isin(ajans)].idxmin()[0]
            worse_new_action=actions.loc[actions[actions['actions']!=duplicated_action].index==actions.loc[actions['actions']!=duplicated_action,worse_agent].idxmax(),'actions']
            recent_actions.loc[recent_actions.agents==worse_agent,'actions']=worse_new_action
        
        if recent_actions.actions.isnull().any():
            agent_null=recent_actions.loc[recent_actions.actions.isnull(),'agents'].values[0]
            forbid_actions=list(recent_actions.actions)
            null_new_action_index=actions.loc[(~actions.actions.isin(forbid_actions)),agent_null].idxmax()
            null_new_action=actions.loc[actions.index==null_new_action_index,'actions']
            recent_actions.loc[recent_actions.agents==agent_null,'actions']=null_new_action.values[0]
            
        left_actions=list(actions.actions)
        current_actions=recent_actions.actions
        while len(actions[actions.actions.isin(recent_actions.actions)])<3:
            left_agent_1=agent_1_oncul[agent_1_oncul.isin(actions.actions)]
            left_agent_2=agent_2_oncul[agent_2_oncul.isin(actions.actions)]
            left_agent_3=agent_3_oncul[agent_3_oncul.isin(actions.actions)]
            if len(left_agent_1)>0 and len(left_agent_2) and len(left_agent_3)>0 and not left_agent_1.isin(recent_actions.actions).all()  and not left_agent_2.isin(recent_actions.actions).all() and not left_agent_3.isin(recent_actions.actions).all():
                for i in current_actions:
                    if i not in left_actions:
                        ended_agent=recent_actions.loc[recent_actions.actions==i,'agents'].values[0]
                        ended_actions=oncul[~oncul[ended_agent].isin(recent_actions.actions)][ended_agent]
                        ended_actions=ended_actions[ended_actions.notna()]
                        new_action_index=actions[actions['actions'].isin(ended_actions)][ended_agent].idxmax()
                    
                        new_action=actions.loc[actions.index==new_action_index,'actions'].values[0]
                        recent_actions.loc[recent_actions.agents==ended_agent,'actions']=new_action
            else:
                for i in current_actions:
                    if i not in left_actions:
                        ended_agent=recent_actions.loc[recent_actions.actions==i,'agents'].values[0]
                        action_max_index=actions[ended_agent].idxmax()
                        new_action=actions.loc[actions.index==action_max_index,'actions'].values[0]
                        worse_choice=actions[actions.actions!=new_action].loc[actions[actions.actions!=new_action][ended_agent].idxmax(),'actions']
                        if len(recent_actions.loc[recent_actions.actions==new_action,'agents'])>0:
                            old_agent=recent_actions.loc[recent_actions.actions==new_action,'agents'].values[0]
                            q_1=agent_actions.loc[agent_actions.index==old_agent,new_action].values[0]
                            q_2=agent_actions.loc[agent_actions.index==ended_agent,new_action].values[0]                                 
                            new_action_expected=actions.loc[actions.actions==new_action,ended_agent].values[0]
                            worse_choice_expected=actions.loc[actions.actions==worse_choice,ended_agent].values[0]
                            total_round=real_rounds.loc[actions[actions.actions==new_action].index].values[0]
                            left_round=actions.loc[actions.actions==new_action,'real_round'].values[0]
                            penalty_new_action = k*total_round*actions.loc[actions.actions==new_action,'unit_utility'].values[0]
                            new_point = new_action_expected - penalty_new_action/left_round
                            
                        if len(recent_actions.loc[recent_actions.actions==worse_choice,'agents'])>0:
                            worse_choice_expected=actions.loc[actions.actions==worse_choice,ended_agent].values[0]                        
                            old_agent_1=recent_actions.loc[recent_actions.actions==worse_choice,'agents'].values[0]
                            q_1_1=agent_actions.loc[agent_actions.index==old_agent_1,worse_choice].values[0]
                            q_2_1=agent_actions.loc[agent_actions.index==ended_agent,worse_choice].values[0]
                            worst_choice=actions[~actions.actions.isin(recent_actions.actions)].loc[actions[~actions.actions.isin(recent_actions.actions)][ended_agent].idxmax(),'actions']
                            worst_choice_expected=actions.loc[actions.actions==worst_choice,ended_agent].values[0]
                            total_round_1=real_rounds.loc[actions[actions.actions==worse_choice].index].values[0]
                            left_round_1=actions.loc[actions.actions==worse_choice,'real_round'].values[0]
                            penalty_worse_action = k*total_round_1*actions.loc[actions.actions==worse_choice,'unit_utility'].values[0]
                            worse_point = worse_choice_expected - penalty_worse_action/left_round_1
                            worst_choice=actions[~actions.actions.isin(recent_actions.actions)].loc[actions[~actions.actions.isin(recent_actions.actions)][ended_agent].idxmax(),'actions']
                            
                        if new_action not in recent_actions.actions.values[:] and new_action not in beginning_actions:
                            recent_actions.loc[recent_actions.agents==ended_agent,'actions']=new_action
                            
                        elif new_action in recent_actions.actions.values[:] and new_action not in beginning_actions and new_action not in changed_actions and q_2>q_1 and new_point>worse_choice_expected:
                            recent_actions.loc[recent_actions.agents==ended_agent,'actions']=new_action
                            actions.loc[actions.actions==new_action,ended_agent]=new_action_expected - penalty_new_action/left_round
                            old_agent_new=actions[~actions.actions.isin(recent_actions.actions)].loc[actions[~actions.actions.isin(recent_actions.actions)][old_agent].idxmax(),'actions']
                            recent_actions.loc[recent_actions.agents==old_agent,'actions']=old_agent_new
                            changed_actions.append(new_action)
                            
                            
            
                        elif worse_choice not in recent_actions.actions.values[:] and worse_choice not in beginning_actions:
                            recent_actions.loc[recent_actions.agents==ended_agent,'actions']=worse_choice
                            
                        elif worse_choice in recent_actions.actions.values[:] and worse_choice not in beginning_actions and worse_choice not in changed_actions and q_2_1>q_1_1 and worse_point>worst_choice_expected:                       
                            changed_actions.append(worse_choice)
                            recent_actions.loc[recent_actions.agents==ended_agent,'actions']=worse_choice
                            actions.loc[actions.actions==worse_choice,ended_agent]=worse_choice_expected - penalty_worse_action/left_round_1
                            old_agent1_new=actions[~actions.actions.isin(recent_actions.actions)].loc[actions[~actions.actions.isin(recent_actions.actions)][old_agent_1].idxmax(),'actions']
                            recent_actions.loc[recent_actions.agents==old_agent_1,'actions']=old_agent1_new                        
                                
                        else:
                            worst_choice=actions[~actions.actions.isin(recent_actions.actions)].loc[actions[~actions.actions.isin(recent_actions.actions)][ended_agent].idxmax(),'actions']                    
                            recent_actions.loc[recent_actions.agents==ended_agent,'actions']= worst_choice
                            
        e_1=recent_actions.loc[recent_actions.agents=='agent_1','actions'].values[0]
        e1.append(e_1)
        u_1=actions.loc[actions.actions==e_1,'agent_1'].values[0]
        u1.append(u_1)
        
        e_2=recent_actions.loc[recent_actions.agents=='agent_2','actions'].values[0]
        e2.append(e_2)
        u_2=actions.loc[actions.actions==e_2,'agent_2'].values[0]
        u2.append(u_2)
        
        e_3=recent_actions.loc[recent_actions.agents=='agent_3','actions'].values[0]
        e3.append(e_3)
        u_3=actions.loc[actions.actions==e_3,'agent_3'].values[0]
        u3.append(u_3)
        
        
        actions.loc[actions.actions==e_1, 'real_round'] = actions.loc[actions.actions==e_1,'real_round'] - 1 
        actions.loc[actions.actions==e_2, 'real_round'] = actions.loc[actions.actions==e_2,'real_round'] - 1
        actions.loc[actions.actions==e_3, 'real_round'] = actions.loc[actions.actions==e_3,'real_round'] - 1
        
        for i in actions.actions:
            if actions.loc[actions.actions==i,"real_round"].values[0]==0:
                finished_actions.append(i)
        
        actions=actions.loc[actions.real_round>0,:]
   
    
    if len(actions[actions.actions==e_1])>0:
        for i in range(int(actions.loc[actions.actions==e_1,'real_round'].values[0])):
            e1.append(e_1)
            u1.append(u_1)

    if len(actions[actions.actions==e_2])>0:
        for i in range(int(actions.loc[actions.actions==e_2,'real_round'].values[0])):
            e2.append(e_2)
            u2.append(u_2)

    if len(actions[actions.actions==e_3])>0:
        for i in range(int(actions.loc[actions.actions==e_3,'real_round'].values[0])):
            e3.append(e_3)
            u3.append(u_3)

    e1=pd.DataFrame(e1,columns=['actions'])
    e2=pd.DataFrame(e2,columns=['actions'])
    e3=pd.DataFrame(e3,columns=['actions'])
                    
    u1=np.cumsum(u1)
    u2=np.cumsum(u2)
    u3=np.cumsum(u3)

    e1['utility_1']=u1
    e2['utility_2']=u2
    e3['utility_3']=u3
    passive_greedy=pd.concat([e1,e2,e3],axis=1,ignore_index=True)
    passive_greedy.columns=['actions_1','utility_1','actions_2','utility_2','actions_3','utility_3']
    passive_greedy=passive_greedy.fillna(method='ffill')
    passive_greedy['toplam']=passive_greedy['utility_1'] + passive_greedy['utility_2'] + passive_greedy['utility_3']

    return passive_greedy,changed_actions
