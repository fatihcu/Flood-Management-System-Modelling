def prep(actions,factors,factor_actions):
    types=pd.DataFrame({'types':['social','economic','environmental']})
    types['agent_1']=[0.5,0.25,0.25]
    types['agent_2']=[0.25,0.5,0.25]
    types['agent_3']=[0.25,0.25,0.5]
    
    types["agent_1"]= types["agent_1"]/(types["agent_1"].max())
    types["agent_2"]= types["agent_2"]/(types["agent_2"].max())
    types["agent_3"]= types["agent_3"]/(types["agent_3"].max())

    
    agents=types.iloc[:,1:].T
    
    actions['difference']=actions['good']-actions['bad']
    actions['real_round']=actions['current']*actions['round']
    action_type=actions[['social','economic','environmental']]/100
    action_type.index=actions['actions']
    action_type=action_type.T
    
    for i in (action_type.columns):
        action_type[i]=action_type[i]/action_type[i].max()
        
        agent_actions=pd.DataFrame(np.dot(agents,action_type))
        agent_actions.columns=actions['actions']
        agent_actions.index=agents.index
        
    for i in (agent_actions.columns):
        agent_actions[i]=agent_actions[i]/agent_actions[i].max()
    b=[]

    for i in list(factor_actions.columns):
        a=factor_actions.loc[(pd.notna(factor_actions[i])),i]
        for j in a:
            b.append([float((factors[factors['factor']==i]['weight_factor'].values)) * float(actions[actions['actions']==j]['difference'].values),j,i])
         
    c=pd.DataFrame(b,columns=['value','action','factor'])
    c=pd.merge(c,factors, on=["factor"]) 
    d=[]        
    for i in c['factor']:
        for j in c[c['factor']==i]['action']:
            #e=[float(c[(c['factor']==i) & (c['action']==j)]['value'].values)/(float(np.sum(np.asarray(c[c['factor']==i]['value'])))),j,i]
            e=[c[(c['factor']==i) & (c['action']==j)]['value'].values[0]*c[c["factor"]==i]["weight_factor"].values[0]/np.sum(np.asarray(c[c['factor']==i]['value'])),j,i]
            
            d.append(e)
    d=pd.DataFrame(d,columns=['value','action','factor'])        
    dd=[]
    for i in list(d['action'].uniagent_actionsue()):
        dd.append([i,np.sum(d[d['action']==i]['value'].values * actions[actions['actions']==i]['current'].values)])
            
    dd=pd.DataFrame(dd,columns=['action','value'])    
    dd['value']=dd['value']/np.sum(dd['value'])
    
    
    ee=[]
    for i in dd['action']:
        if actions[actions['actions']==i]['real_round'].values==0:
            ee.append([i,0])
        else:
            ee.append([i,(dd[dd['action']==i]['value'].values[0])/(actions[actions['actions']==i]['real_round'].values[0])])
    ee=pd.DataFrame(ee,columns=['actions','unit_utility'])

    actions=actions.merge(ee,on='actions')


    actions['total_utility']=actions['unit_utility']*actions['real_round']
    


    return actions,agent_actions
