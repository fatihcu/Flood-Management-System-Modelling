# Flood-Management-System-Modelling

Models aims to optimize institutions' actions to avoid flood disasters devistating effects. These are sample codes written by me for an academic work made by two researchers at Yildiz Technical University.

1 variable preparation process and 7 different optimization methods are defined in py files.

Requirements

Pandas
Numpy

To make such analysis, you need to have a factors dataset which have specific factors affecting disaster management like rebuilding infrastucture or educating neighborhood people and in that dataset weights of importance must be defined. 
Secondly, you need to have factor-actions dataset which must have factors and actions to do specific factors. 
Lastly, actions data is necessary in which each actions' good and bad effects, round to be completed e.g. months and these actions' importance by three different aspects; social, economic and environmental.

After preparation function ran with these infos, you get two results; transformed action dataframe and agent_action dataframe. Then you just need to run optimization method you select.

# Approach Definitons

There are three main approaches defined in this work.

In greedy based approaches, agents (institutions) can interrupt others' ongoing work and take it over. Their first motivation is maximizing their own utility. There four types greedy optimization method; Greedy-Greedy, Greedy-Social, Greedy-Zeuthen and Greedy-Objective, others are Passive-Passive, Passive-Greedy and Coward

Greedy-Greediy: Agents solely seek to maximize utility, there is no other constraints.

Greedy-Social: While taking an action from another agent, agents must take care social benefits and a restriction added

Greedy-Zeuthen: In this method, a risk function is defined and agents calculate the risk function to take an action from another agent

Greedy-Objective: In this method, every agents' targets are defined according to action that they are best at doing it. Agents' 
interrupting process changes by how their utilities are far from their targets at that moment.

Passive-Passive: Agents do what they are best at. There is no interruption

Passive-Greedy: Agents do what they best at until one of them has no other action to do, after that game turns to Greedy-Greedy style

Coward Aproach: Agents calculate what if i take this action after finishing the recent one and if there is possibility to be 
interrupted, there is no interruption
