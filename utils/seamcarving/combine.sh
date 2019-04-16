#!/bin/bash
ffmpeg -framerate 15 -i out/ratatouille_frames/res_%02d.png -vf format=yuv420p ratatouille1_combined.mp4