#!/usr/bin/env python
# coding: utf-8

# In[1]:


#FINAL CODE STARTS HERE


# In[1]:


import pickle
import snap


# In[ ]:


#---Global variables as parameters
macroInfluencer = 200000
microInfluencer = 100000
#Maximum Number of influencers By Type
numberOfMacro = 0
numberOfMicro = 10
desiredReach = 2000000

macroSelected = 0
microSelected = 0
#---end global variables


# In[ ]:


def DeleteSelected(followersMap, completeGraph, i):
    for node in followersMap[i]:
        if completeGraph.IsNode(node) and node not in followersMap:
            completeGraph.DelNode( node )
    del followersMap[i]
    return followersMap

def MacroMicro(followersMap, i):
    global macroInfluencer
    global microInfluencer
    global macroSelected
    global microSelected
    if len(followersMap[i]) > macroInfluencer:
        macroSelected+=1
    elif len(followersMap[i]) > microInfluencer:
        microSelected+=1
    if macroSelected > numberOfMacro:
        return True
    if microSelected > numberOfMicro:
        return True

def LoadGraph(name):
    if name.split(".")[-1]=="graph":
        FIn = snap.TFIn("res/others/" + name )
        completeGraph = snap.TUNGraph.Load( FIn )   
    else:
        FIn = snap.TFIn("res/others/" + name + ".graph" )
        completeGraph = snap.TUNGraph.Load( FIn )   
    return completeGraph
def SaveGraph(graph, name):
    if name.split(".")[-1]=="graph":
        FOut = snap.TFOut("res/others/" + name)
        graph.Save( FOut )
        FOut.Flush()
    else:
        FOut = snap.TFOut("res/others/" + name + ".graph")
        graph.Save( FOut )  
        FOut.Flush()
    return


# In[271]:


def NumberMappings( influencers, followers):
    influencerNumberMap = {}
    followerNumberMap = {}
    count = 0
    for i in influencers.keys():
        influencerNumberMap[i]=count
        count+=1
    count = 0
    for j in followers.keys():
        followerNumberMap[j]=count
        count+=1
        
    #Required Format
    followersMap = {}
    for i in influencers:
        influencerNumberCode = influencerNumberMap[i]
        followersMap[influencerNumberCode]=[]
        for j in influencers[i]:
            try:
                followersMap[influencerNumberCode].append(followerNumberMap[j])
            except Exception as e:
                print e    
    return influencerNumberMap, followerNumberMap, followersMap


# In[272]:


def GenerateGraph(followersMap):
    completeGraph = snap.TUNGraph.New()
    count = 0
    for i in followersMap:
        if not completeGraph.IsNode( i ):
            completeGraph.AddNode( i )
            count+=1
        for j in followersMap[i]:
            if not completeGraph.IsNode( j ):
                completeGraph.AddNode( j )
                count+=1
            completeGraph.AddEdge( i, j )
    return completeGraph


# In[265]:


def SelectBestTwo(followersMap):    
    shortlistedInfluencers = []
    maxAudience = 0
    selectedInfluencerA = ''
    selectedInfluencerB = ''
    visitedNodes = []
    for i in followersMap:
        #-------------------
        #print i
        #Load Last state of the Graph
        #FIn = snap.TFIn("res/others/completeGraph.graph")
        #completeGraph = snap.TUNGraph.Load( FIn )
        completeGraph = LoadGraph(  "completeGraph" )        
        #---looping conditions start
        #Checking category of Influencer
        macroSelected = 0
        microSelected = 0
        if MacroMicro( followersMap, i ):
            continue       
        #Storing Degree of Influencer under consideration
        audienceA = completeGraph.GetNI(i).GetDeg()
        #Remove all followers of Influencer from the graph
        for node in followersMap[ i ]:
            if node not in followersMap:
                completeGraph.DelNode(node)
        visitedNodes.append( i )
        #Calculate Audience with all other influencers
        #----------------------------------------------
        for j in followersMap:
            #-------------------    
            if j in visitedNodes or MacroMicro( followersMap, j ) or i==j:
                continue
            #Calculating Category
            audienceSize = audienceA+completeGraph.GetNI(j).GetDeg()
            if audienceSize > maxAudience:
                maxAudience = audienceSize
                selectedInfluencerA = i
                selectedInfluencerB = j
        #----------------------------------------------
    print selectedInfluencerA , "  -  " , selectedInfluencerB
    shortlistedInfluencers = [ selectedInfluencerA, selectedInfluencerB ]
    print "Max Audience Possible: " + str( maxAudience )
    print "Select Inf is :", shortlistedInfluencers
    #---remove edges of selected influncers
    #Remove nodes of selected Influencers
    completeGraph =  LoadGraph("completeGraph")
    if len(followersMap[shortlistedInfluencers[0]])>macroInfluencer or len(followersMap[shortlistedInfluencers[1]])>macroInfluencer:
        macroSelected+=1
    elif len(followersMap[shortlistedInfluencers[0]])>microInfluencer or len(followersMap[shortlistedInfluencers[1]])>microInfluencer:
        microSelected+=1            
    for i in shortlistedInfluencers:
        followersMap  = DeleteSelected(followersMap,completeGraph, i)
    #Save updated State
    SaveGraph(completeGraph, "completeGraph")
    #print shortlistedInfluencers
    #print maxAudience
    return shortlistedInfluencers, maxAudience, followersMap


# In[267]:


def GetOptimumCombination(followersMap, shortlistedInfluencers, maxAudience):
    while len(followersMap)>0:
        currentAudience = maxAudience
        if currentAudience > desiredReach:
            print "Max Desired Audeince Reached!."
            break
        audience=0
        selectedInfluencer = -1
        for i in followersMap:
            #Influencer Category
            if MacroMicro( followersMap, i ):
                continue
            #Load Last state of the Graph
            completeGraph = LoadGraph("completeGraph")
            #Storing Degree of Influencer under consideration
            audience = completeGraph.GetNI( i ).GetDeg()
            audienceSize = currentAudience + audience
            if not audienceSize < maxAudience:
                maxAudience = audienceSize
                selectedInfluencer = i
        if selectedInfluencer==-1:
            break
        shortlistedInfluencers.append(selectedInfluencer)

        if len(followersMap[selectedInfluencer])>macroInfluencer:
            macroSelected+=1
        elif len(followersMap[selectedInfluencer])>microInfluencer:
            microSelected+=1            
        followersMap = DeleteSelected( followersMap,completeGraph, selectedInfluencer )
        #Save updated State    
        SaveGraph(completeGraph, "completeGraph")
        print "Influncers: ", shortlistedInfluencers
        print "Reach: ", maxAudience


# In[277]:

import sys
def Main():
    #print "Arguments: ", sys.argv
    #---we should have following argument if any of them is missing than use default values 
    #---Global variables as parameters
    global  macroInfluencer
    global microInfluencer
    global numberOfMacro
    global numberOfMicro
    global desiredReach
    global macroSelected
    global microSelected
    #---end global variables
    #TargetedReach=100000 MacroThreshold=200000 MicroThreshold=10000 MaxMacroAllowed=2 MaxMicroAllowed=3
    args = sys.argv
    for i in range(1, len(args)):
        try:
            a = args[i].split("=")[0]
            v = args[i].split("=")[1]
        except Exception as e:
            print e
            continue
        if a=="TargetedReach":
            desiredReach = v

        if a=="MacroThreshold":
            macroInfluencer = v

        if a=="MicroThreshold":
            microInfluencer = v

        if a=="MaxMacroAllowed":
            numberOfMacro = v

        if a=="MaxMicroAllowed":
            numberOfMicro = v
                
    print "Running With Arguments: ", {  "TargetedReach" : desiredReach, "MacroThreshold" : macroInfluencer, "MicroThreshold" : microInfluencer, "MaxMacroAllowed" : numberOfMacro, "MaxMicroAllowed" : numberOfMicro }
    print "Note: Make sure you have res/others folder in same directory containing all inputs..."
    print "---------------------------------------------------------------------------------------------------------"
    print "Processing Start Wait for a while..."
    #Reading Data
    followers = pickle.load( open( "res/others/followers_15.pickle", "rb" ) )
    print "Total Followers: " , len(followers.keys())
    influencers = pickle.load( open( "res/others/giantPool_15.pickle", "rb" ) )
    print "Total Influencers: " , len(influencers.keys())
    #-----filter only five influncers for testing purpose of below code, delete others
    """
    iter = 0 
    for k in influencers.keys():
        iter+=1
        if iter>=5:
            del influencers[k]
    """    
    print "Generating Mapings..."
    influencerNumberMap, followerNumberMap, followersMap = NumberMappings( influencers, followers)
    print "Generating Graph..."
    completeGraph = GenerateGraph( followersMap )
    SaveGraph(completeGraph, "completeGraph" )
    print 'Graph Saved...'
    print "Graph Nodes: ", completeGraph.GetNodes()
    print "Graph Edges: ", completeGraph.GetEdges()
    print "Selecting Initial Influencers..."
    shortlistedInfluencers, maxAudience, followersMap = SelectBestTwo( followersMap )
    print "Finding Optimal Combinations..."
    GetOptimumCombination(followersMap, shortlistedInfluencers, maxAudience)


# In[278]:


Main()


# In[ ]:





# In[ ]:





# In[ ]:




