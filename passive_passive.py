def passive_strategy(actions,agent_action):
    
        agent_1_primes=[]    
        agent_2_primes=[]
        agent_3_primes=[]

        for i in list(agent_action.columns):
            if agent_action.loc[(agent_action.index=='agent_1'),i].values==1:
                agent_1_primes.append(i)
            elif agent_action.loc[(agent_action.index=='agent_2'),i].values==1:
                agent_2_primes.append(i)
            else:
                agent_3_primes.append(i)
        agent_1_target=np.sum(actions[actions['actions'].isin(agent_1_primes)]['total_utility'])
        agent_2_target=np.sum(actions[actions['actions'].isin(agent_2_primes)]['total_utility'])
        agent_3_target=np.sum(actions[actions['actions'].isin(agent_3_primes)]['total_utility'])
        
        scores_1=[]
        for i in agent_1_primes:
            scores_1.append([float(actions[actions['actions']==i]['unit_utility'].values),i])
        scores_1=pd.DataFrame(scores_1,columns=['unit_utility','actions'])
        scores_1=scores_1.sort_values(by='unit_utility',ascending=False)
        agent_1_df=[]
        for i in list(scores_1['actions']):
            for j in np.arange(int(actions.loc[actions['actions']==i,'real_round'].values)):
                agent_1_df.append([ float(scores_1[scores_1['actions']==i]['unit_utility'].values), i] )
        agent_1_df=pd.DataFrame(agent_1_df, columns=['utility_1','actions_1'])
        agent_1_df=agent_1_df[agent_1_df['utility_1']!=0]
        agent_1_df['utility_1']=np.cumsum(agent_1_df['utility_1'])
        
        scores_2=[]
        for i in agent_2_primes:
            scores_2.append([float(actions[actions['actions']==i]['unit_utility'].values),i])
        scores_2=pd.DataFrame(scores_2,columns=['unit_utility','actions'])
        scores_2=scores_2.sort_values(by='unit_utility',ascending=False)
        agent_2_df=[]
        for i in list(scores_2['actions']):
            for j in np.arange(int(actions.loc[actions['actions']==i,'real_round'].values)):
                agent_2_df.append([ float(scores_2[scores_2['actions']==i]['unit_utility'].values), i] )
        agent_2_df=pd.DataFrame(agent_2_df, columns=['utility_2','actions_2'])
        agent_2_df=agent_2_df[agent_2_df['utility_2']!=0]
        agent_2_df['utility_2']=np.cumsum(agent_2_df['utility_2'])
        
        scores_3=[]
        for i in agent_3_primes:
            scores_3.append([float(actions[actions['actions']==i]['unit_utility'].values),i])
        scores_3=pd.DataFrame(scores_3,columns=['unit_utility','actions'])
        scores_3=scores_3.sort_values(by='unit_utility',ascending=False)
        agent_3_df=[]
        for i in list(scores_3['actions']):
            for j in np.arange(int(actions.loc[actions['actions']==i,'real_round'].values)):
                agent_3_df.append([ float(scores_3[scores_3['actions']==i]['unit_utility'].values), i] )
        agent_3_df=pd.DataFrame(agent_3_df, columns=['utility_3','actions_3'])
        agent_3_df=agent_3_df[agent_3_df['utility_3']!=0]
        agent_3_df['utility_3']=np.cumsum(agent_3_df['utility_3'])
        passive_passive=pd.concat([agent_1_df,agent_2_df,agent_3_df],axis=1)
        passive_passive=passive_passive.fillna(method='ffill')
        passive_passive['total']=passive_passive['utility_1'] + passive_passive['utility_2'] + passive_passive['utility_3']

        return passive_passive



