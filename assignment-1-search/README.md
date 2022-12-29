# HW1‚ Search

## Back Story

You work at a food delivery startup called BigByte. The company consists of two people, Shobhana and you, both alumni of the Life Institute located in Heavanston. You take care of software development and Shobhana handles the rest. 

BigByte's target client restaurants and ordering customers are all based in Heavanston, which has a handful of landmarks and a heavily fluctuating traffic pattern. To ensure that your delivery fleet works efficiently, Shobhana has asked you to come up with a route planning system. 

Fortunately, Heavanston restaurants and residents' homes are close to landmarks, so you only need to tell delivery drivers how best to reach one landmark from another. You have a map of all Heavanston roads and data from a traffic survey maintained by University Archives. For you, that means you only need to write three (3) more pieces of software before the launch: an implementation of each of **Breadth-first Search (BFS)**, **Depth-first Search (DFS)**, and the **A\* algorithm** that all find the best way to travel between any pair of landmarks in town. You're implementing three algorithms because you want to eventually do a comparative analysis of all three to select the best one.

## Task Parameters

A diagram explaining the relative position of major landmarks of Heavanston is shown below. 

<img src="map.png" width="60%">

Shobhana has supplied you with a few different maps you can use to develop the software. These maps can be found in the `a_star_gradingtests.py` file. The file also has tests that you can use to test your software. **Shobhana is only going to accept your work if your code passes all the tests.** Additionally, in order to test the robustness of your software, **Shobhana may also use some additional tests that she's not willing to show you now.** They will be different from the tests with which she's supplied you, but similar enough that if your implementation is correct, it should pass the unseen tests too as long as you don't use any shortcuts (e.g., hardcoding, writing code specifically aimed at passing the tests while not implementing the desired algorithm, etc.) 

Things to note about the maps:

1. If you look at the test functions, you'll see that certain tests use certain maps. Please be mindful of that.

2. With DFS, once a node is expanded, it must not show up again further down that same branch. However, the same node can show up on different branches of the tree, which means in the entire search, the same node can be expanded more than once. That said, the maps for DFS don't have any loops, so it is not necessary to keep a list of expanded nodes. In fact, if you keep a list of expanded nodes, it will result in incorrect answers, so do not keep such a list.

3. The maps for BFS, however, may contain loops, so it's best to maintain a list of expanded nodes. Shobhana reminds you that Russell and Norvig’s book *Artificial Intelligence: A Modern Approach* describes BFS in some detail.

4. While Shobhana would love for each of your algorithms to find the best route it could find from the restaurant to the customer, she understands it may not necessarily do that. As stated in #6 below, the main metric each algorithm will use is the time difference between places, which means the best route is the fastest one. For the given problems, BFS and A* will succeed in finding the fastest routes by virtue of how the algorithms work, but DFS is not guaranteed to find the fastest route, and you shouldn't worry about it.

5. When a node is expanded, the order in which its children nodes are added to the fringe will determine if the search will traverse the tree from left to right or right to left. Either direction of traversal is acceptable, i.e., the test functions will accept correct results from either direction of traversal.

6. Your A\* function will be given two routing maps as inputs. The first map specifies the straight-line distance between two landmarks; we will refer to this as the **distance map**. The second map is based on the data from the Archives traffic survey. It specifies the expected time it takes a driver to go from one landmark to a neigbhoring landmark; we will refer to this as the **time map**. For all three implementations (BFS, DFS, and A\*), you will use the time differences between places as the main metric, not distance. However, for A\*, you will use the distances between places as the **heuristic** (how far you're from the destination). In other words, for A\*, the distance from the start to your current location will be time-based, but the estimated distance from your current location to the destination will be distance-based.

7. With A\*, if two or more nodes have the same f(n), you should use h(n) to break the tie, i.e., pick the node that has the smallest h(n). If two or more nodes have the same h(n), then pick the node that entered the open list first when returned/yielded by expand(). If you're using a priority queue, then the order of the nodes will not be preserved due to sorting, so you may need to use a separate variable to keep track of the order.

When passed to your A\* implementation, both the distance map and the time map are stored in the same format (a Python dictionary). The following is an example time map.

```python
Time_map = {
'Campus':
	{'Campus':None,'Whole_Food':4,'Beach':3,'Cinema':None,'Lighthouse':1,'Ryan Field':None,'YWCA':None},
'Whole_Food':
	{'Campus':4,'Whole_Food':None,'Beach':4,'Cinema':3,'Lighthouse':None,'Ryan Field':None,'YWCA':None},
'Beach':
	{'Campus':4,'Whole_Food':4,'Beach':None,'Cinema':None,'Lighthouse':None,'Ryan Field':None,'YWCA':None},
'Cinema':
	{'Campus':None,'Whole_Food':4,'Beach':None,'Cinema':None,'Lighthouse':None,'Ryan Field':None,'YWCA':2},
'Lighthouse':
	{'Campus':1,'Whole_Food':None,'Beach':None,'Cinema':None,'Lighthouse':None,'Ryan Field':1,'YWCA':None},
'Ryan Field':
	{'Campus':None,'Whole_Food':None,'Beach':None,'Cinema':None,'Lighthouse':2,'Ryan Field':None,'YWCA':5},
'YWCA':
	{'Campus':None,'Whole_Food':None,'Beach':None,'Cinema':3,'Lighthouse':None,'Ryan Field':5,'YWCA':None}}
```

In this example, the traffic time between Campus and Beach is `3`. `None` indicates that there is no road that directly connects the two landmarks. Off-road driving is prohibited by local law, so drivers must only take the roads marked on the diagram above. Combining this legal requirement with the volatile traffic pattern of Heavanston, it is certain that the distance map can only be used as a heuristic for the A\* algorithm. It is also noteworthy that the time it takes traveling in alternate directions on the same road is most likely different.

## Homework Deliverable

For this homework, you must implement all three (3) functions in `student_code.py`. Each function must return a path from landmark `start` to landmark `end`.

**The tests provided with this homework assume the use of Python 3. We recommend Python 3.6 or above.**

Note that:

* The result must be a list of strings. Each string contains _only_ the name of a landmark. The order of the strings in the list denotes the order in which the landmarks are reached along the path;
* The result list should _begin_ with the name of the `start` landmark and _terminate_ with the name of the `end` landmark. (Thus, the path from `A` to `A` is the list `[A]`);
* The cost of a path between two connected landmarks is the total expected traffic time that must be spent travelling all landmarks in the order specified by the path.

Your `a_star_search` function must implement an A\* **graph** search algorithm, and it must use the `expand` function in `expand.py`. With the `expand` function, we can verify that the correct number of nodes is expanded. As a reminder, graph search algorithms do not expand nodes that have already been visited.

Your BFS and DFS implementations will essentially be **tree** search algorithms operating on the graphs that the maps form. Right, the maps are graphs, but for BFS and DFS, you will implement tree searches on those graphs. Now, just because they are tree searches, it doesn't mean nodes already visited can be expanded -- they can for DFS (see #2 under Task Parameters), but that is incorrect behavior for BFS.

Furthermore, the Autograder that Shobhana will use to test your code assumes that all of the code that is needed to properly grade your assignment submission is included in `student_code.py`. Please adhere to this constraint as you develop your response.

Additionally, you should feel invited to use Python modules for your data structures, but you need to implement A\* yourself.

## Testing the code

1. To test the code run the following commands to test the corresponding functions,
	1. ```python3 dfs_test.py```
	2. ```python3 bfs_test.py```
	3. ```python3 a_star_test.py```
