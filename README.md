# InfluencerOverlap
# Package Versions: </br>
    python=Python 2.7.15 :: Anaconda, Inc.</br>
    pickle=$Revision: 72223 $</br>
    snap=4.1.0-dev-Win-x64-py2.7</br>

   
# Installation:
1. To install SNAP follow "https://snap.stanford.edu/snappy/" it have installation instruction for Linux, Windows, Mac etc.
2. To install python via anaconda follow "https://www.anaconda.com/distribution/#download-section" select python 2.7. 
3. If you have anaconda 3.7 installed than make an environment for python 2.7 and than install SNAP inside that environment.
4. Installation of SNAP through pip is **not** recommended.

# Run:
1. Make sure you have directory as res/others in same directory in which SNAP--Audience Overlap_V1.1 located.
2. Make sure all inputs i.e giantPool.pickle and followers.pickle files are in res/others no other inputs are required.
3. To Pass Custom argument like number of micro influncers etc edit runV1.0 file.
4. If you do not want to pass an argument than simply remove it program will use its default values.
5. For all parameters default values are TargetedReach=2000000 MacroThreshold=300000 MicroThreshold=100000 MaxMacroAllowed=0 MaxMicroAllowed=10.
6. Remeber there are total five argumets and you can pass them in any order or can skip any of them or all of them. 
7. For example if you want to run program with all default values than type in cmd (python "SNAP--Audience Overlap_V1.1.py") with out any argument.
8. To run from cmd use command (python "SNAP--Audience Overlap_V1.1.py" TargetedReach=100000 MacroThreshold=300000 MicroThreshold=150000 MaxMacroAllowed=1 MaxMicroAllowed=5).
9. Make sure res/others have write permission for user from which you are running python program.
