# BernardJelly
## Project Summary
These Python projects, created by [Bernard Chan]( https://github.com/bernardmc8), are centered around improving the efficiency and speed of the video analysis pipeline for UC Berkeley Professor Richard Harland's Jellydreamers lab. Jellydreamers aims to understand the function of sleep in jellyfish through wet-lab experiments and tracking jellyfish pulse activity using Python video analysis and data science techniques. 

## Program Functionality
### [PulseLocator.py]( https://github.com/bernardmc8/BernardJelly/blob/master/PulseLocator.py)
Jellydreamers' jellyfish analysis involves recording the timing of jellyfish pulses and locating the ganglia that propagates each pulse. Since the research is focused on tracking jellyfish pulses, PulseLocator.py aims to filter the jellyfish recordings, removing the frames in which the jellyfish is not pulsing before the recordings enter the video analysis pipeline. On average, this program cuts the number of frames in a given jellyfish recording by 600%, resulting in a massive, 600% increase in the speed of the video analysis pipeline. 

<img src="https://i.ibb.co/272ZVp1/Screenshot-10.png"
     alt="Jellyfish Analysis" />


### [Automatedsteps.py]( https://github.com/bernardmc8/BernardJelly/blob/master/automatedsteps.py)
Presently, operating the video analysis pipeline involves a lab researcher manually configuring and starting each step of the pipeline multiple times for a single video. This current method is not very user-friendly, and requires life science researchers to memorize a convulted process of copying/pasting code into a terminal, running various scripts, and creating/altering files. Not only does this cause many technical issues, but it requires a researcher to tend to the computer every hour or so to start the next step of the pipeline. Automatedsteps.py aims to automate key manual steps of the video analysis pipeline so that lab researchers can input multiple videos at a time and the pipeline can run continuously overnight or over the weekend, greatly minimizing downtime and increasing efficiency. 

<img src="https://i.ibb.co/CHX7DzP/Screenshot-6.png"
     alt="Jellyfish Analysis" />
