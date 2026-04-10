---
source_type: web
title: "API reference - simple-pid 2.0.0"
author: 
created_at: 2026-04-06
topics:
  - 待分类
status: inbox
source: "https://simple-pid.readthedocs.io/en/latest/reference.html"
published: 
created: 2026-04-06
description: 
tags:
  - 
  - "clippings"
---

## API reference

This library consists of only one class, `PID`, which you make an instance of and use. It’s full API documentation is given below.

## simple\_pid.PID

*class* simple\_pid.pid.PID [\[source\]](https://simple-pid.readthedocs.io/en/latest/_modules/simple_pid/pid.html#PID) [#](#simple_pid.pid.PID "Permalink to this definition")

A simple PID controller.

\_\_init\_\_(*Kp=1.0*, *Ki=0.0*, *Kd=0.0*, *setpoint=0*, *sample\_time=0.01*, *output\_limits=(None, None)*, *auto\_mode=True*, *proportional\_on\_measurement=False*, *differential\_on\_measurement=True*, *error\_map=None*, *time\_fn=None*, *starting\_output=0.0*) [\[source\]](https://simple-pid.readthedocs.io/en/latest/_modules/simple_pid/pid.html#PID.__init__) [#](#simple_pid.pid.PID.__init__ "Permalink to this definition")

Initialize a new PID controller.

Parameters:

- **Kp** – The value for the proportional gain Kp
- **Ki** – The value for the integral gain Ki
- **Kd** – The value for the derivative gain Kd
- **setpoint** – The initial setpoint that the PID will try to achieve
- **sample\_time** – The time in seconds which the controller should wait before generating a new output value. The PID works best when it is constantly called (eg. during a loop), but with a sample time set so that the time difference between each update is (close to) constant. If set to None, the PID will compute a new output value every time it is called.
- **output\_limits** – The initial output limits to use, given as an iterable with 2 elements, for example: (lower, upper). The output will never go below the lower limit or above the upper limit. Either of the limits can also be set to None to have no limit in that direction. Setting output limits also avoids integral windup, since the integral term will never be allowed to grow outside of the limits.
- **auto\_mode** – Whether the controller should be enabled (auto mode) or not (manual mode)
- **proportional\_on\_measurement** – Whether the proportional term should be calculated on the input directly rather than on the error (which is the traditional way). Using proportional-on-measurement avoids overshoot for some types of systems.
- **differential\_on\_measurement** – Whether the differential term should be calculated on the input directly rather than on the error (which is the traditional way).
- **error\_map** – Function to transform the error value in another constrained value.
- **time\_fn** – The function to use for getting the current time, or None to use the default. This should be a function taking no arguments and returning a number representing the current time. The default is to use time.monotonic() if available, otherwise time.time().
- **starting\_output** – The starting point for the PID’s output. If you start controlling a system that is already at the setpoint, you can set this to your best guess at what output the PID should give when first calling it to avoid the PID outputting zero and moving the system away from the setpoint.

\_\_call\_\_(*input\_*, *dt=None*) [\[source\]](https://simple-pid.readthedocs.io/en/latest/_modules/simple_pid/pid.html#PID.__call__) [#](#simple_pid.pid.PID.__call__ "Permalink to this definition")

Update the PID controller.

Call the PID controller with *input\_* and calculate and return a control output if sample\_time seconds has passed since the last update. If no new output is calculated, return the previous output instead (or None if no value has been calculated yet).

Parameters:

**dt** – If set, uses this value for timestep instead of real time. This can be used in simulations when simulation time is different from real time.

*property* components [#](#simple_pid.pid.PID.components "Permalink to this definition")

The P-, I- and D-terms from the last computation as separate components as a tuple. Useful for visualizing what the controller is doing or when tuning hard-to-tune systems.

*property* tunings [#](#simple_pid.pid.PID.tunings "Permalink to this definition")

The tunings used by the controller as a tuple: (Kp, Ki, Kd).

*property* auto\_mode [#](#simple_pid.pid.PID.auto_mode "Permalink to this definition")

Whether the controller is currently enabled (in auto mode) or not.

set\_auto\_mode(*enabled*, *last\_output=None*) [\[source\]](https://simple-pid.readthedocs.io/en/latest/_modules/simple_pid/pid.html#PID.set_auto_mode) [#](#simple_pid.pid.PID.set_auto_mode "Permalink to this definition")

Enable or disable the PID controller, optionally setting the last output value.

This is useful if some system has been manually controlled and if the PID should take over. In that case, disable the PID by setting auto mode to False and later when the PID should be turned back on, pass the last output variable (the control variable) and it will be set as the starting I-term when the PID is set to auto mode.

Parameters:

- **enabled** – Whether auto mode should be enabled, True or False
- **last\_output** – The last output, or the control variable, that the PID should start from when going from manual mode to auto mode. Has no effect if the PID is already in auto mode.

*property* output\_limits [#](#simple_pid.pid.PID.output_limits "Permalink to this definition")

The current output limits as a 2-tuple: (lower, upper).

See also the *output\_limits* parameter in.

reset() [\[source\]](https://simple-pid.readthedocs.io/en/latest/_modules/simple_pid/pid.html#PID.reset) [#](#simple_pid.pid.PID.reset "Permalink to this definition")

Reset the PID controller internals.

This sets each term to 0 as well as clearing the integral, the last output and the last input (derivative calculation).