---
source_type:
source: "https://github.com/Gurobi/modeling-examples"
title: "Gurobi/modeling-examples: Gurobi modeling examples"
author:
published_at:
created_at: "2026-04-24T00:07:53+08:00"
topics: "Gurobi modeling examples. Contribute to Gurobi/modeling-examples development by creating an account on GitHub."
tags:
  - "clippings"
related_concepts:
status: "inbox"
---
[![[gurobi-light.png|Gurobi]]](https://www.gurobi.com/)

## Target audience

Data scientists, engineers, computer scientists, economists, and in general, professionals with a background in mathematical modeling and a basic knowledge of Python.

## Goals of modeling examples

- Illustrate the broad applicability of mathematical optimization.
- Show how to build mathematical optimization models.

These modeling examples are coded using the Gurobi Python API and distributed as Jupyter Notebooks.

These modeling examples illustrate important capabilities of the Gurobi Python API, including adding decision variables, building linear expressions, adding constraints, and adding an objective function. They touch on more advanced features such as generalized constraints, piecewise-linear functions, and multi-objective hierarchical optimization. They also illustrate common constraint types such as “allocation constraints”, “balance constraints”, “sequencing constraints”, “precedence constraints”, and others.

The examples are from different business purposes and reflect different levels of building mathematical optimization models.

## Introductory examples

The introductory examples walk you through the process of building a mathematical optimization model. The basic requirements are that you know Python and have a background in a discipline that uses quantitative methods.

- [Intro to Gurobipy:](https://github.com/Gurobi/modeling-examples/blob/master/intro_to_gurobipy) This tutorial was given at the Gurobi Days Digital 2023. It is an introduction to the Gurobi Python API Gurobipy. It walks you through the basics of Gurobipy and explains its usage with some small examples.
- [Intro to Mathematical Optimization Modeling:](https://github.com/Gurobi/modeling-examples/blob/master/milp_tutorial) This tutorial discusses the basics of mathematical modeling on the example of a simple assignment problem.
- [Optimization 101:](https://github.com/Gurobi/modeling-examples/blob/master/optimization101) This tutorial is based on the Webinar on [Optimization 101 for Data Scientists](https://www.gurobi.com/events/optimization-101-for-data-scientists/) and consists of two modeling sessions with exercises and questions as well as a discussion of a use case.
- The following examples discuss the input data and the optimization model step by step in a very detailed way
	- [Airline Planning After Flight Disruption](https://github.com/Gurobi/modeling-examples/blob/master/aviation_planning)
		- [Music Recommendation](https://github.com/Gurobi/modeling-examples/blob/master/music_recommendation)
		- [Text Dissimilarity](https://github.com/Gurobi/modeling-examples/blob/master/text_dissimilarity)
		- [Power Generation](https://github.com/Gurobi/modeling-examples/blob/master/power_generation)

## Beginner Examples

The notebooks at the beginner level assume you know Python and have some knowledge about building mathematical optimization models.

- [3D Tic-Tac-Toe:](https://github.com/Gurobi/modeling-examples/blob/master/3d_tic_tac_toe) This example will show you how a binary programming model can be used to capture simple logical constraints.
- [Battery Scheduling:](https://github.com/Gurobi/modeling-examples/blob/master/battery_scheduling) This example shows how you can build a simple battery scheduling model that involves energy balance equations, state-of-charge dynamics, and nonlinear objectives.
- [Cell Tower:](https://github.com/Gurobi/modeling-examples/blob/master/cell_tower_coverage) In this example, you will learn how to define and solve a covering-type problem, namely, how to configure a network of cell towers to provide signal coverage to the largest number of people.
- [Curve Fitting:](https://github.com/Gurobi/modeling-examples/blob/master/curve_fitting) Try this Jupyter Notebook Modeling Example to learn how you can fit a function to a set of observations.
- [Facility Location:](https://github.com/Gurobi/modeling-examples/blob/master/facility_location) In this example, we will show you how to tackle a facility location problem that involves determining the number and location of warehouses that are needed to supply a group of supermarkets.
- [Fantasy Basketball:](https://github.com/Gurobi/modeling-examples/blob/master/fantasy_basketball) This example combines machine learning and optimization modeling in fantasy basketball.
- [Food Program:](https://github.com/Gurobi/modeling-examples/blob/master/food_program) Transporting food in a global transportation network is a challenging undertaking. In this notebook, we will build an optimization model to set up a food supply chain based on real data from the UN World Food Program.
- [Market Sharing:](https://github.com/Gurobi/modeling-examples/blob/master/market_sharing) In this example, we will show you how to solve a goal programming problem that involves allocating the retailers to two divisions of a company in order to optimize the trade-offs of several market-sharing goals.
- [Marketing Campaign Optimization:](https://github.com/Gurobi/modeling-examples/blob/master/marketing_campaign_optimization) Companies across almost every industry are looking to optimize their marketing campaigns. In this Jupyter Notebook, we will explore a marketing campaign optimization problem that is common in the banking and financial services industry, which involves determining which products to offer to individual customers in order to maximize total expected profit while satisfying various business constraints.
- [Offshore Wind Farming:](https://github.com/Gurobi/modeling-examples/blob/master/offshore_wind_farming) In this example, we will learn how to solve an offshore wind power generation problem. The goal of the problem is to figure out which underwater cables should be laid to connect an offshore wind farm power network at a minimum cost.
- [Supply Network Design 1:](https://github.com/Gurobi/modeling-examples/blob/master/supply_network_design) Try this Jupyter Notebook Modeling Example to learn how to solve a classic supply network design problem that involves finding the minimum cost flow through a network. We will show you how – given a set of factories, depots, and customers – you can use mathematical optimization to determine the best way to satisfy customer demand while minimizing shipping costs. In part 2, we additionally determine which depots to open or close in order to minimize overall costs.

## Intermediate Examples

Examples at the intermediate level assume that you know Python and are familiar with the Gurobi Python API. In addition, you should have knowledge about building mathematical optimization models.

- [Agricultural Pricing:](https://github.com/Gurobi/modeling-examples/blob/master/agricultural_pricing) Try this example to learn how to use mathematical optimization to tackle a common, but critical agricultural pricing problem: Determining the prices and demand for a country’s dairy products in order to maximize total revenue derived from the sales of those products. You will learn how to model this problem as a quadratic optimization problem using the Gurobi Python API and solve it using the Gurobi Optimizer.
- [Linear Regression:](https://github.com/Gurobi/modeling-examples/blob/master/linear_regression) In this example, you will learn how to perform linear regression with feature selection using mathematical programming. We will show you how to construct a mixed-integer quadratic programming (MIQP) model of this linear regression problem.
- [Car Rental:](https://github.com/Gurobi/modeling-examples/blob/master/car_rental) This notebook will teach you how you can use mathematical optimization to figure out how many cars a car rental company should own and where they should be located every day to maximize weekly profits. Part 2 considers an extension on how mathematical optimization can be used to figure out in which locations a car rental company should expand repair capacity.
- [Customer Assignment:](https://github.com/Gurobi/modeling-examples/blob/master/customer_assignment) This notebook is an intermediate version of the facility location problem. In addition, we show how machine learning can be used in the pre-processing so as to reduce the computational burden of big datasets.
- [Economic Planning:](https://github.com/Gurobi/modeling-examples/blob/master/economic_planning) In this example, you will discover how mathematical optimization can be used to address a macroeconomic planning problem that a country may face. The goal is to determine different possible growth patterns for the economy.
- [Efficiency Analysis:](https://github.com/Gurobi/modeling-examples/blob/master/efficiency_analysis) How can mathematical optimization be used to measure the efficiency of an organization? Find out in this example, where you will learn how to formulate an Efficiency Analysis model as a linear programming problem.
- [Electrical Power Generation:](https://github.com/Gurobi/modeling-examples/blob/master/electrical_power_generation) This model is an example of an electrical power generation problem (also known as a unit commitment problem). It selects an optimal set of power stations to turn on in order to satisfy anticipated power demand over a 24-hour time horizon. In part 2, the model is extended and adds the option of using hydroelectric power plants to satisfy demand.
- [Factory Planning:](https://github.com/Gurobi/modeling-examples/blob/master/factory_planning) In this example, we create an optimal production plan that maximizes profits. In part 2, we create an optimal production plan that will not only maximize profits but also determine the months in which to perform maintenance operations on the machines.
- [Food Manufacturing:](https://github.com/Gurobi/modeling-examples/blob/master/food_manufacturing) You will learn how to create an optimal multi-period production plan for a product that requires a number of ingredients – each of which has different costs, restrictions, and features. In part 2, additional constraints are considered that change the problem type from a linear program (LP) problem to a mixed-integer program (MIP) problem, making it harder to solve.
- [Logical Design:](https://github.com/Gurobi/modeling-examples/blob/master/logical_design) In this example, you will learn how to solve a logical design problem, which involves constructing a circuit using the minimum number of NOR gates (devices with two inputs and one output) that will perform the logical function specified by a truth table.
- [Mining:](https://github.com/Gurobi/modeling-examples/blob/master/mining) In this example, you will learn how to model and solve a multi-period production planning problem that involves optimizing the operations of a group of mines over a five-year period.
- [Opencast Mining:](https://github.com/Gurobi/modeling-examples/blob/master/opencast_mining) This notebook shows a mathematical optimization problem to identify which excavation locations to choose in order to maximize the gross margins of extracting ore.
- [Power Generation:](https://github.com/Gurobi/modeling-examples/blob/master/power_generation) Assume that we know the set of all available power plants and the demand for power for each hour of a day. We want to create a schedule to decide how much power each plant should generate, and when to switch the plants “on” and “off” in order to minimize the overall costs.
- [Refinery:](https://github.com/Gurobi/modeling-examples/blob/master/refinery) This model is an example of a production planning problem where decisions must be made regarding which products to produce and which resources to use.
- [Technician Routing and Scheduling:](https://github.com/Gurobi/modeling-examples/blob/master/technician_routing_scheduling) Try this modeling example to discover how mathematical optimization can help telecommunications firms automate and improve their technician assignment, scheduling, and routing decisions in order to ensure the highest levels of customer satisfaction. You will learn how to formulate a multi-depot vehicle routing problem with time windows constraints.

## Advanced Examples

For modeling examples at the advanced level, we assume that you know Python and the Gurobi Python API and that you have advanced knowledge of building mathematical optimization models. Typically, the objective function and/or constraints of these examples are complex or require advanced features of the Gurobi Python API.

- [Constraint Optimization:](https://github.com/Gurobi/modeling-examples/blob/master/constraint_optimization) In this example, we consider a constraint of an integer programming model where all the decision variables in the constraint are binary, the goal is to find another constraint involving the same binary variables that is logically equivalent to the original constraint, but that has the smallest possible absolute value of the right-hand side.
- [Decentralization Planning:](https://github.com/Gurobi/modeling-examples/blob/master/decentralization_planning) This model is an advanced version of a facility location problem. Given a set of departments of a company and potential cities where these departments can be located, we want to determine the "best" location of each department in order to maximize gross margins.
- [Farm Planning:](https://github.com/Gurobi/modeling-examples/blob/master/farm_planning) This is an example of an advanced production planning problem.
- [Index Tracking:](https://github.com/Gurobi/modeling-examples/blob/master/index_tracking) Index tracking portfolio optimization.
- [Lost Luggage Distribution:](https://github.com/Gurobi/modeling-examples/blob/master/lost_luggage_distribution) This is an example of a vehicle routing problem with time windows. It involves helping a company figure out the minimum number of vans required to deliver pieces of lost or delayed baggage to their rightful owners and determining the optimal assignment of vans to customers.
- [Manpower Planning:](https://github.com/Gurobi/modeling-examples/blob/master/manpower_planning) This notebook solves a staffing planning problem where choices must be made regarding recruitment, training, redundancy, and scheduling of staff.
- [Milk Collection:](https://github.com/Gurobi/modeling-examples/blob/master/milk_collection) This is an example of a capacitated vehicle routing problem. With only one tanker truck with limited capacity, you will need to determine the best possible route for the tanker to take to collect milk every day from a set of farms.
- [Portfolio Selection Optimization:](https://github.com/Gurobi/modeling-examples/blob/master/portfolio_selection_optimization) This model is an example of the classic Markowitz portfolio selection optimization model. We want to find the fraction of the portfolio to invest among a set of stocks that balances risk and return. It is a Quadratic Programming (QP) model with vector and matrix data for returns and risk, respectively.
- [Pooling:](https://github.com/Gurobi/modeling-examples/blob/master/pooling) Companies across numerous industries – including petrochemical refining, wastewater treatment, and mining – use mathematical optimization to solve the pooling problem. This problem can be regarded as a generalization of the minimum-cost flow problem and the blending problem.
- [Protein Comparison:](https://github.com/Gurobi/modeling-examples/blob/master/protein_comparison) You will learn how to model the protein comparison problem as a quadratic assignment problem. It involves measuring the similarities of two proteins.
- [Protein Folding:](https://github.com/Gurobi/modeling-examples/blob/master/protein_folding) The problem pertains to a protein, which consists of a chain of amino acids. The objective is to predict the optimum folding of the chain.
- [Railway Dispatching:](https://github.com/Gurobi/modeling-examples/blob/master/railway_dispatching) In this notebook, we look at dispatching of trains sharing resources (tracks and stations) with limited capacity. The objective is to minimize delays.
- [Traveling Salesman:](https://github.com/Gurobi/modeling-examples/blob/master/traveling_salesman) This notebook covers one of the most famous combinatorial optimization problems in existence: the Traveling Salesman Problem (TSP). The goal of the TSP – to find the shortest possible route that visits each city once and returns to the original city – is simple, but solving the problem is a complex and challenging endeavor. This example uses the [callback](https://www.gurobi.com/documentation/current/refman/py_cb_s.html) feature of Gurobi.
- [Workforce Scheduling:](https://github.com/Gurobi/modeling-examples/blob/master/workforce) In this notebook, we demonstrate how you can use mathematical optimization to generate an optimal workforce schedule that minimizes the number of temporary workers your company needs to hire and maximizes employee fairness. The problem is formulated as a multi-objective mixed-integer-programming (MIP) model and uses the [multiple objectives feature](https://www.gurobi.com/documentation/current/refman/multiple_objectives.html) of Gurobi.
- [Yield Management:](https://github.com/Gurobi/modeling-examples/blob/master/yield_management) In this example, we will show you how an airline can use AI technology to devise an optimal seat pricing strategy. You will learn how to formulate this Yield Management Problem as a three-period stochastic programming problem.

## Examples via Business Needs

Automation
- [Marketing Campaign Optimization](https://github.com/Gurobi/modeling-examples/blob/master/marketing_campaign_optimization) (beginner)
- [Supply Network Design](https://github.com/Gurobi/modeling-examples/blob/master/supply_network_design) (beginner)
- [Technician Routing and Scheduling](https://github.com/Gurobi/modeling-examples/blob/master/technician_routing_scheduling) (intermediate)
- [Manpower Planning](https://github.com/Gurobi/modeling-examples/blob/master/manpower_planning) (advanced)
- [Workforce Scheduling](https://github.com/Gurobi/modeling-examples/blob/master/workforce) (advanced)
Customer Management
- [Supply Network Design](https://github.com/Gurobi/modeling-examples/blob/master/supply_network_design) (beginner)
- [Covid19 Facility Optimization](https://github.com/Gurobi/modeling-examples/blob/master/covid19_facility_location) (beginner)
- [Yield Management](https://github.com/Gurobi/modeling-examples/blob/master/yield_management) (advanced)
Forecasting
- [Price Optimization](https://github.com/Gurobi/modeling-examples/blob/master/price_optimization) (introductory)
- [Music Recommendation](https://github.com/Gurobi/modeling-examples/blob/master/music_recommendation) (introductory)
- [Fantasy Basketball](https://github.com/Gurobi/modeling-examples/blob/master/fantasy_basketball) (beginner)
- [Covid19 Facility Optimization](https://github.com/Gurobi/modeling-examples/blob/master/covid19_facility_location) (beginner)
- [Agricultural Pricing](https://github.com/Gurobi/modeling-examples/blob/master/agricultural_pricing) (intermediate)
- [Linear Regression](https://github.com/Gurobi/modeling-examples/blob/master/linear_regression) (intermediate)
Inventory Optimization
- [Price Optimization](https://github.com/Gurobi/modeling-examples/blob/master/price_optimization) (introductory)
- [Food Program](https://github.com/Gurobi/modeling-examples/blob/master/food_program) (beginner)
- [Car Rental](https://github.com/Gurobi/modeling-examples/blob/master/car_rental) (intermediate)
- [Economic Planning](https://github.com/Gurobi/modeling-examples/blob/master/economic_planning) (intermediate)
- [Factory Planning](https://github.com/Gurobi/modeling-examples/blob/master/factory_planning) (intermediate)
- [Food Manufacturing](https://github.com/Gurobi/modeling-examples/blob/master/food_manufacturing) (intermediate)
- [Farm Planning](https://github.com/Gurobi/modeling-examples/blob/master/farm_planning) (advanced)
Location Planning
- [Cell Tower](https://github.com/Gurobi/modeling-examples/blob/master/cell_tower_coverage) (beginner)
- [Facility Location](https://github.com/Gurobi/modeling-examples/blob/master/facility_location) (beginner)
- [Car Rental](https://github.com/Gurobi/modeling-examples/blob/master/car_rental) (intermediate)
- [Customer Assignment](https://github.com/Gurobi/modeling-examples/blob/master/customer_assignment) (intermediate)
- [Opencast Mining](https://github.com/Gurobi/modeling-examples/blob/master/opencast_mining) (intermediate)
- [Decentralization Planning](https://github.com/Gurobi/modeling-examples/blob/master/decentralization_planning) (advanced)
Logistics
- [Price Optimization](https://github.com/Gurobi/modeling-examples/blob/master/price_optimization) (introductory)
- [Supply Network Design](https://github.com/Gurobi/modeling-examples/blob/master/supply_network_design) (beginner)
- [Food Program](https://github.com/Gurobi/modeling-examples/blob/master/food_program) (beginner)
- [Traveling Salesman](https://github.com/Gurobi/modeling-examples/blob/master/traveling_salesman) (advanced)
Marketing
- [Music Recommendation](https://github.com/Gurobi/modeling-examples/blob/master/music_recommendation) (introductory)
- [Marketing Campaign Optimization](https://github.com/Gurobi/modeling-examples/blob/master/marketing_campaign_optimization) (beginner)
- [Customer Assignment](https://github.com/Gurobi/modeling-examples/blob/master/customer_assignment) (intermediate)
Network Optimization
- [Airline Planning After Flight Disruption](https://github.com/Gurobi/modeling-examples/blob/master/aviation_planning) (introductory)
- [Food Program](https://github.com/Gurobi/modeling-examples/blob/master/food_program) (beginner)
- [Supply Network Design](https://github.com/Gurobi/modeling-examples/blob/master/supply_network_design) (beginner)
Operations
- [Airline Planning After Flight Disruption](https://github.com/Gurobi/modeling-examples/blob/master/aviation_planning) (introductory)
- [Battery Scheduling](https://github.com/Gurobi/modeling-examples/blob/master/battery_scheduling) (beginner)
- [Price Optimization](https://github.com/Gurobi/modeling-examples/blob/master/price_optimization) (introductory)
- [Covid19 Facility Optimization](https://github.com/Gurobi/modeling-examples/blob/master/covid19_facility_location) (beginner)
- [Power Generation](https://github.com/Gurobi/modeling-examples/blob/master/power_generation) (intermediate)
Portfolio Management
- [Portfolio Selection Optimization](https://github.com/Gurobi/modeling-examples/blob/master/portfolio_selection_optimization) (advanced)
- [Index Tracking](https://github.com/Gurobi/modeling-examples/blob/master/index_tracking) (advanced)
Production
- [Economic Planning](https://github.com/Gurobi/modeling-examples/blob/master/economic_planning) (intermediate)
- [Efficiency Analysis](https://github.com/Gurobi/modeling-examples/blob/master/efficiency_analysis) (intermediate)
- [Electrical Power Generation](https://github.com/Gurobi/modeling-examples/blob/master/electrical_power_generation) (intermediate)
- [Factory Planning](https://github.com/Gurobi/modeling-examples/blob/master/factory_planning) (intermediate)
- [Food Manufacturing](https://github.com/Gurobi/modeling-examples/blob/master/food_manufacturing) (intermediate)
- [Mining](https://github.com/Gurobi/modeling-examples/blob/master/mining) (intermediate)
- [Power Generation](https://github.com/Gurobi/modeling-examples/blob/master/power_generation) (intermediate)
- [Refinery](https://github.com/Gurobi/modeling-examples/blob/master/refinery) (intermediate)
- [Farm Planning](https://github.com/Gurobi/modeling-examples/blob/master/farm_planning) (advanced)
Research
- [Curve Fitting](https://github.com/Gurobi/modeling-examples/blob/master/curve_fitting) (beginner)
- [Linear Regression](https://github.com/Gurobi/modeling-examples/blob/master/linear_regression) (intermediate)
- [Efficiency Analysis](https://github.com/Gurobi/modeling-examples/blob/master/efficiency_analysis) (intermediate)
- [Constraint Optimization](https://github.com/Gurobi/modeling-examples/blob/master/constraint_optimization) (intermediate)
Resource
- [Price Optimization](https://github.com/Gurobi/modeling-examples/blob/master/price_optimization) (introductory)
- [Economic Planning](https://github.com/Gurobi/modeling-examples/blob/master/economic_planning) (intermediate)
- [Electrical Power Generation](https://github.com/Gurobi/modeling-examples/blob/master/electrical_power_generation) (intermediate)
- [Power Generation](https://github.com/Gurobi/modeling-examples/blob/master/power_generation) (intermediate)
- [Food Manufacturing](https://github.com/Gurobi/modeling-examples/blob/master/food_manufacturing) (intermediate)
- [Farm Planning](https://github.com/Gurobi/modeling-examples/blob/master/farm_planning) (advanced)
- [Yield Management](https://github.com/Gurobi/modeling-examples/blob/master/yield_management) (advanced)
Routing
- [Food Program](https://github.com/Gurobi/modeling-examples/blob/master/food_program) (beginner)
- [Technician Routing and Scheduling](https://github.com/Gurobi/modeling-examples/blob/master/technician_routing_scheduling) (intermediate)
- [Lost Luggage Distribution](https://github.com/Gurobi/modeling-examples/blob/master/lost_luggage_distribution) (advanced)
- [Milk Collection](https://github.com/Gurobi/modeling-examples/blob/master/milk_collection) (advanced)
- [Traveling Salesman](https://github.com/Gurobi/modeling-examples/blob/master/traveling_salesman) (advanced)
Sales Optimization
- [Price Optimization](https://github.com/Gurobi/modeling-examples/blob/master/price_optimization) (introductory)
- [Marketing Campaign Optimization](https://github.com/Gurobi/modeling-examples/blob/master/marketing_campaign_optimization) (beginner)
- [Customer Assignment](https://github.com/Gurobi/modeling-examples/blob/master/customer_assignment) (intermediate)
- [Food Manufacturing](https://github.com/Gurobi/modeling-examples/blob/master/food_manufacturing) (intermediate)
Supply Chain
- [Market Sharing](https://github.com/Gurobi/modeling-examples/blob/master/market_sharing) (beginner)
- [Supply Network Design](https://github.com/Gurobi/modeling-examples/blob/master/supply_network_design) (beginner)
- [Food Program](https://github.com/Gurobi/modeling-examples/blob/master/food_program) (beginner)
- [Power Generation](https://github.com/Gurobi/modeling-examples/blob/master/power_generation) (intermediate)
- [Traveling Salesman](https://github.com/Gurobi/modeling-examples/blob/master/traveling_salesman) (advanced)
Allocation/Scheduling
- [Technician Routing and Scheduling](https://github.com/Gurobi/modeling-examples/blob/master/technician_routing_scheduling) (intermediate)
- [Manpower Planning](https://github.com/Gurobi/modeling-examples/blob/master/manpower_planning) (advanced)
- [Traveling Salesman](https://github.com/Gurobi/modeling-examples/blob/master/traveling_salesman) (advanced)
- [Railway Dispatching](https://github.com/Gurobi/modeling-examples/blob/master/railway_dispatching) (advanced)
- [Workforce Scheduling](https://github.com/Gurobi/modeling-examples/blob/master/workforce) (advanced)

It is also possible to browse through the examples w.r.t. difficulty level and business needs on the [Gurobi website](https://www.gurobi.com/jupyter_models/).

## Run on Google Colab

You can access all the examples in Google Colab, which is a free, online Jupyter Notebook environment that allows you to write and execute Python code through your browser. You will need to be signed into a Google account to execute the notebooks. But you do not need an account if you just want to look at the notebooks. For each example, the respective colab link is given in the readme:

- To run the example the first time, choose “Runtime” and then click “Run all”.
- All the cells in the Jupyter Notebook will be executed.
- The example will install the gurobipy package. The Gurobi pip package includes a size-limited trial license equivalent to the Gurobi "online course" license. For most of the notebooks, this restricted license is sufficient to run them. For others, you will need a full license, see the license section below.
- You can also modify and re-run individual cells.
- For subsequent runs, choose “Runtime” and click “Restart and run all”.
- The Gurobi Optimizer will find the optimal solution of the modeling example. Check out the [Colab Getting Started Guide](https://colab.research.google.com/notebooks/intro.ipynb#scrollTo=GJBs_flRovLc) for full details on how to use Colab Notebooks as well as create your own.

## Run locally

- Clone the repository containing all examples or download it by clicking [here](https://github.com/Gurobi/modeling-examples/archive/refs/heads/master.zip)
- [Start Jupyter Notebook Server](https://docs.jupyter.org/en/latest/running.html#id2)
- Open the particular notebook in Jupyter Notebook.
- The notebook will install the gurobipy package and other dependencies. The Gurobi pip package includes a size-limited trial license equivalent to the Gurobi "online course" license. For most of the notebooks, this restricted license is sufficient. For others, you will need a full license.

## Licensing

In order to run the Jupyter Notebooks you will need a Gurobi license. Most of the notebooks can be run using the "online course" license version of Gurobi. This is a limited license and restricts the number of allowed variables and constraints. This restricted license comes also with the gurobipy package when installing it via pip or conda. You can also request a full license, i.e., an [evaluation license](https://www.gurobi.com/downloads/request-an-evaluation-license/) as a *commercial user*, or download a [free license](https://www.gurobi.com/academia/academic-program-and-licenses/) as an *academic user*. The latter two license types allow you to run all notebooks. All licenses can also be requested in the [Gurobi User Portal](https://portal.gurobi.com/iam/licenses/request/) after [registering for a Gurobi account](https://portal.gurobi.com/iam/register/).

## Download the repository

You can download the repository containing all examples by clicking [here](https://github.com/Gurobi/modeling-examples/archive/master.zip).

## Index of modeling examples

- [3D Tic-Tac-Toe](https://github.com/Gurobi/modeling-examples/blob/master/3d_tic_tac_toe)
- [Airline Planning After Flight Disruption](https://github.com/Gurobi/modeling-examples/blob/master/aviation_planning)
- [Agricultural Pricing](https://github.com/Gurobi/modeling-examples/blob/master/agricultural_pricing)
- [Battery Scheduling](https://github.com/Gurobi/modeling-examples/blob/master/battery_scheduling)
- [Burrito Game](https://github.com/Gurobi/modeling-examples/blob/master/burrito_optimization_game)
- [Car Rental](https://github.com/Gurobi/modeling-examples/blob/master/car_rental)
- [Cell Tower](https://github.com/Gurobi/modeling-examples/blob/master/cell_tower_coverage)
- [Cutting Stock](https://github.com/Gurobi/modeling-examples/blob/master/colgen-cutting_stock)
- [Constraint Optimization](https://github.com/Gurobi/modeling-examples/blob/master/constraint_optimization)
- [Covid19 Facility Optimization](https://github.com/Gurobi/modeling-examples/blob/master/covid19_facility_location)
- [Curve Fitting](https://github.com/Gurobi/modeling-examples/blob/master/curve_fitting)
- [Customer Assignment](https://github.com/Gurobi/modeling-examples/blob/master/customer_assignment)
- [Decentralization Planning](https://github.com/Gurobi/modeling-examples/blob/master/decentralization_planning)
- [Drone Network](https://github.com/Gurobi/modeling-examples/blob/master/drone_network)
- [Economic Planning](https://github.com/Gurobi/modeling-examples/blob/master/economic_planning)
- [Efficiency Analysis](https://github.com/Gurobi/modeling-examples/blob/master/efficiency_analysis)
- [Electrical Power Generation](https://github.com/Gurobi/modeling-examples/blob/master/electrical_power_generation)
- [Facility Location](https://github.com/Gurobi/modeling-examples/blob/master/facility_location)
- [Factory Planning](https://github.com/Gurobi/modeling-examples/blob/master/factory_planning)
- [Fantasy Basketball](https://github.com/Gurobi/modeling-examples/blob/master/fantasy_basketball)
- [Farm Planning](https://github.com/Gurobi/modeling-examples/blob/master/farm_planning)
- [Food Manufacturing](https://github.com/Gurobi/modeling-examples/blob/master/food_manufacturing)
- [Food Program](https://github.com/Gurobi/modeling-examples/blob/master/food_program)
- [Index Tracking](https://github.com/Gurobi/modeling-examples/blob/master/index_tracking)
- [Intro to Gurobipy](https://github.com/Gurobi/modeling-examples/blob/master/intro_to_gurobipy)
- [Intro to Mathematical Optimization Modeling / MILP Tutorial](https://github.com/Gurobi/modeling-examples/blob/master/milp_tutorial)
- [Linear Regression](https://github.com/Gurobi/modeling-examples/blob/master/linear_regression)
- [Logical Design](https://github.com/Gurobi/modeling-examples/blob/master/logical_design)
- [Lost Luggage Distribution](https://github.com/Gurobi/modeling-examples/blob/master/lost_luggage_distribution)
- [Manpower Planning](https://github.com/Gurobi/modeling-examples/blob/master/manpower_planning)
- [Market Sharing](https://github.com/Gurobi/modeling-examples/blob/master/market_sharing)
- [Marketing Campaign Optimization](https://github.com/Gurobi/modeling-examples/blob/master/marketing_campaign_optimization)
- [Milk Collection](https://github.com/Gurobi/modeling-examples/blob/master/milk_collection)
- [Mining](https://github.com/Gurobi/modeling-examples/blob/master/mining)
- [Music Recommendation](https://github.com/Gurobi/modeling-examples/blob/master/music_recommendation)
- [Offshore Wind Farming](https://github.com/Gurobi/modeling-examples/blob/master/offshore_wind_farming)
- [Opencast Mining](https://github.com/Gurobi/modeling-examples/blob/master/opencast_mining)
- [Optimization 101](https://github.com/Gurobi/modeling-examples/blob/master/optimization101)
- [Pooling](https://github.com/Gurobi/modeling-examples/blob/master/pooling)
- [Portfolio Selection Optimization](https://github.com/Gurobi/modeling-examples/blob/master/portfolio_selection_optimization)
- [Power Generation](https://github.com/Gurobi/modeling-examples/blob/master/power_generation)
- [Price Optimization](https://github.com/Gurobi/modeling-examples/blob/master/price_optimization)
- [Protein Comparison](https://github.com/Gurobi/modeling-examples/blob/master/protein_comparison)
- [Protein Folding](https://github.com/Gurobi/modeling-examples/blob/master/protein_folding)
- [Railway Dispatching](https://github.com/Gurobi/modeling-examples/blob/master/railway_dispatching)
- [Refinery](https://github.com/Gurobi/modeling-examples/blob/master/refinery)
- [Supply Network Design](https://github.com/Gurobi/modeling-examples/blob/master/supply_network_design)
- [Technician Routing and Scheduling](https://github.com/Gurobi/modeling-examples/blob/master/technician_routing_scheduling)
- [Text Dissimilarity](https://github.com/Gurobi/modeling-examples/blob/master/text_dissimilarity)
- [Traveling Salesman](https://github.com/Gurobi/modeling-examples/blob/master/traveling_salesman)
- [Workforce Scheduling](https://github.com/Gurobi/modeling-examples/blob/master/workforce)
- [Yield Management](https://github.com/Gurobi/modeling-examples/blob/master/yield_management)

These modeling examples are distributed under the Apache 2.0 license  
© Gurobi Optimization, LLC