import os
import sys

import main
import main_iterative
import main_iterative_all_videos

if __name__ == "__main__":
    video_path = ""
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
        if not os.path.exists(video_path):
            print("Missing file video: video path is not correct")
            exit(0)
        if len(sys.argv) == 2:
            main_iterative.run(video_path)
        else:
            # soglia di durata minima di una fissazione (frame)
            duration_threshold = int(sys.argv[2])
            # soglia di dispersione massima di una fissazione (pixel)
            dispersion_threshold = int(sys.argv[3])
            main.run(video_path, duration_threshold, dispersion_threshold)
    else:
        main_iterative_all_videos.run()



