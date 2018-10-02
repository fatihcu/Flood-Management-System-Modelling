def coward(eylem,ajan_eylem):
    
    agent_1_actions=[]
    agent_2_actions=[]
    agent_3_actions=[]
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
    first_actions={'agents':['agent_1','agent_2','agent_3'],'actions':['B5','B3','B15']}
    first_actions=pd.DataFrame(first_actions)
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

    used=[]
    while len(actions)>3:
        if len(recent_actions.actions.uniagentsue())<3:
            vc=recent_actions.actions.value_counts().reset_index()
            duplicated_action = vc[vc['actions']>1]['index']
            agents=list(recent_actions.loc[recent_actions.actions==duplicated_action.values[0],'agents'])
            worse_agent=agent_actions[agent_actions[duplicated_action].index.isin(agents)].idxmin()[0]
            worse_new_action_index=actions.loc[~actions.actions.isin(recent_actions.actions)][worse_agent].idxmax()
            worse_new_action = actions.loc[worse_new_action_index,'actions']
            recent_actions.loc[recent_actions.agents==worse_agent,'actions']=worse_new_action

        if recent_actions.actions.isnull().any():
            agent_null=recent_actions.loc[recent_actions.actions.isnull(),'agents'].values[0]
            forbid_actions=list(recent_actions.actions)
            null_new_action_index=actions.loc[(~actions.actions.isin(forbid_actions)),agent_null].idxmax()
            null_new_action=actions.loc[actions.index==null_new_action_index,'actions']
            recent_actions.loc[recent_actions.agents==agent_null,'actions']=null_new_action.values[0]

        
        current_actions=list(recent_actions.actions)
        used = used + current_actions
        used = list(set(used))
        failures=[]
        while len(actions[actions.actions.isin(recent_actions.actions)])<3:
            if len(recent_actions.actions.uniagentsue())<3:
                vc=recent_actions.actions.value_counts().reset_index()
                duplicated_action = vc[vc['actions']>1]['index']
                agents=list(recent_actions.loc[recent_actions.actions==duplicated_action.values[0],'agents'])
                worse_agent=agent_actions[agent_actions[duplicated_action].index.isin(agents)].idxmin()[0]
                worse_new_action_index=actions.loc[~actions.actions.isin(recent_actions.actions)][worse_agent].idxmax()
                worse_new_action = actions.loc[worse_new_action_index,'actions']
                recent_actions.loc[recent_actions.agents==worse_agent,'actions']=worse_new_action
           
            for i in recent_actions.actions:
                if i not in actions.actions.values:
                    ended_agent=recent_actions.loc[recent_actions.actions==i,'agents'].values[0]
                    action_max_index=actions.loc[(~actions.actions.isin(failures)) & (~actions.actions.isin(used)),ended_agent].idxmax()
                    new_action=actions.loc[actions.index==action_max_index,'actions'].values[0]
                    new_action_round=actions.loc[actions.actions==new_action,'real_round'].values[0]
                    names = list(recent_actions[recent_actions.agents!=ended_agent]['agents'])
                    other_1=actions[['actions','real_round',names[0]]]    
                    other_1.columns=['actions','real_round','agent']
                    #other_1 = other_1[other_1.actions!=new_action]
                    other_2=actions[['actions','real_round',names[1]]]
                    other_2.columns=['actions','real_round','agent']
                    #other_2 = other_2[other_2.actions!=new_action]
                    other_1=other_1.sort_values(by='agent',ascending=False).reset_index(drop=True)
                    other_2= other_2.sort_values(by='agent',ascending=False).reset_index(drop=True)
                    other_1_df_ix=other_1[other_1.actions==new_action].index[0]
                    other_1_df=other_1.iloc[:other_1_df_ix,:]
                    round_1=np.sum(other_1_df['real_round'])
                    other_2_df_ix=other_2[other_2.actions==new_action].index[0]
                    other_2_df=other_2.iloc[:other_2_df_ix + 1,:]
                    round_2=np.sum(other_2_df['real_round'])
                    agents_ended=agent_actions.loc[ended_agent,new_action]
                    agents_1=agent_actions.loc[names[0],new_action]
                    agents_2 = agent_actions.loc[names[1],new_action]
                    if (agents_ended>agents_1 or new_action_round<=round_1) and (agents_ended>agents_2 or new_action_round<=round_2):
                        recent_actions.loc[recent_actions.agents==ended_agent,'actions']=new_action
                    else:
                        failures.append(new_action)
                
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
        recent_actions['total_utility']=[np.sum(u1),np.sum(u2),np.sum(u3)]        
        
        
        actions.loc[actions.actions==e_1, 'real_round'] = actions.loc[actions.actions==e_1,'real_round'] - 1 
        actions.loc[actions.actions==e_2, 'real_round'] = actions.loc[actions.actions==e_2,'real_round'] - 1
        actions.loc[actions.actions==e_3, 'real_round'] = actions.loc[actions.actions==e_3,'real_round'] - 1
        
        
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
    coward=pd.concat([e1,e2,e3],axis=1,ignore_index=True)
    coward.columns=['actions_1','utility_1','actions_2','utility_2','actions_3','utility_3']
    coward=coward.fillna(method='ffill')
    coward['total']=coward['utility_1'] + coward['utility_2'] + coward['utility_3']
                        
    return coward