2021-02-10 ideal pump

Basic idea : 

Process series of 'Therapy X started, Time T, duration D, amount A' events.
Build up series of (time, amount) points to draw line segments.

Each time a new therapy starts later than prior one, cut prior(s) into two and output a new (time,amount).

{ "Time":0,   "Type":"T1Started", "Amount": 5000, "Duration": 1800 }
{ "Time":120, "Type":"T2Started", "Amount":7000, "Duration":2100 }
{ "Time":360, "Type":"TbfStarted", "Factor":2000, "Duration":900}


