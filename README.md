#Path Planning Algorithms Part 2 Project

Tony Luo
Elton Chen

***Documentation***
So in this project we use Q-Learning to find the most optimal policies. Since this kind of mirrors the previous assignment, just `roslaunch solution_python.launch` via the launch file. It should technically have it's package called `cse_190_final`, so if your ros enviroment is set up correctly, it should just work.
You need to have the images in the img file, because there are the new red dot images.
In the configuration.json files, we have a big and small config. Just `cp configuration_<big/small>.json configuration.json` in `scripts/` to see the output. The video does not render properly, so you want to just manually go through the images. Also you need to add a learning rate of value `float(0.0 to 0.1)` in the .json and if start is `0` instead of `[index of row, index of col]`, it will start randomly.
After running, you will see images in the image file. And you should see the red dots as the paths, S as the start position, and E as the absorption/end state.
