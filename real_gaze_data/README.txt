==CONTENTS==
1. raw_gaze_data - data from eye-tracking device AS IS
2. filtered_gaze_data - filtered data from eye-tracking device (see "Data post-processing" at http://compression.ru/video/savam/)
3. gaussian_vizualizations - disrtibution of gaze locations vizualized with multiple Gaussians
4. Source video can be download from http://compression.ru/video/savam/



==DATA FORMAT==
Format of data in file "list_video.txt":
	videoname [v001..v043]
	sequence {any string}
	start frame in sequence {any positive number}

Format of data in file "list_user.txt": 
	username [u001..u048]
	sex [m, f]
	age [18..56]
	looks number [1..3]
	views order [bwd, fwd]

File names in folders "raw_gaze_data" and "filtered_gaze_data"
	videoname [v001..v043]
	sequence {any string}
	start frame in sequence {any positive number}
	user_name [u001..u048]
	sex [m, f]
	age [18..56]
	trial_number [1..3] *
	views_order [bwd, fwd] **

*  Some observers participated more than one time
** Some observers watched sequence of clips in inverted order. Only order clips was inverted (not frame order of the clips). 
   So you DON'T have to invert this data.
	
Format of data in files from folders "base_before" and "base_after"
	time stamp [1000000000..1040000000] (1000000 ~ 1s, 40000 ~ 1frame)
	left X coord [0..1920] 
	left Y coord [0..1080]
	right X coord [0..1920]
	right Y coord [0..1080]

NOTICE: if X and Y coordinates of gaze position are zero, that means that gaze position is unknown. 
In most cases that means that observer's eyes are closed.


==Questions==
With any questions according usage of this data you can contact 
"Alexey Fedorov" <afedorov@graphics.cs.msu.ru>
