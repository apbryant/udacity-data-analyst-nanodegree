link to gist: http://bl.ocks.org/apbryant/21b9541a19fdfe00309031d0eda6d8ef

# Summary

I used a dataset on car specifications to visualize the relationship between a car's weight in tons and miles per gallon. My visualization consists of two graphs: A scatterplot of a car's weight and mpg, and a scatterplot that colors the points according to how many engine cylinders the car has. Users can click the page to alternate between the two graphs.

The main point of the visualization: heavier cars get worse mpg.

# Design

I used a scatterplot to encode the relationship between weight and mpg. I chose a scatterplot because it is an effective way to show the relationship between two continuous variables. 

In later iterations of the visualization I colored the points based on the number of engine cylinders the cars have. Coloring the points this way highlights a variable that correlates with both mpg and weight, and that could also influence a car's mpg.

Finally, I colored the points a shade of blue to make them easier on the eyes to view and reduced the points' opacity to make it easier to view overlapping points.

# Feedback

## Person 1: 
My first design was just the first scatterplot of weight and mpg. I received feedback from a fellow DAND student who understood the relationship I wanted to communicate, and suggested that I include animation and try to include other variables in my visualization. I followed the advice by creating a second scatterplot that colored points based upon how many cylinders they have as well as created a way for users to cycle between the two plots. 

## Person 2:
A friend who works on his own data projects said my chart was fine, suggested that I label points, such as outliers. I didn't do anything in response to this because the visualization already provides details about specific points, and there aren't any outliers in the data.

## Person 3:
On my second iteration of the chart, another Udacity student commented saying that my chart would be better if I made the points of the first chart the same color. Having different colors obscured the message I want to convey. I took their advice and made the change.