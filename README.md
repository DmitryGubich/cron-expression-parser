# Cron Expression Parser Task

Write a command line application or script which parses a cron string and expands each field
to show the times at which it will run. You may use whichever language you feel most
comfortable with.

Please do not use existing cron parser libraries for this exercise. Whilst it’s generally a good
idea to use pre-built libraries, we want to assess your ability to create your own!

You should only consider the standard cron format with five time fields (minute, hour, day of
month, month, and day of week) plus a command, and you do not need to handle the special
time strings such as `"@yearly"`. The input will be on a single line.

The cron string will be passed to your application as a single argument:

`~$ your-program "d"`

The output should be formatted as a table with the field name taking the first 14 columns and
the times as a space-separated list following it.

For example, the following input argument:
`*/15 0 1,15 * 1-5 /usr/bin/find`

Should yield the following output:
```
minute 0 15 30 45
hour 0
day of month 1 15
month 1 2 3 4 5 6 7 8 9 10 11 12
day of week 1 2 3 4 5
command /usr/bin/find
```

You should spend no more than three hours on this exercise. If you do not have time to
handle all possible cron strings then an app which handles a subset of them correctly is
better than one which does not run or produces incorrect results. You will be asked to extend
the solution with additional features in the interview, so please have your development
environment ready in the way you like it, ready for screen sharing.

You should see your project reviewer as a new team member you are handling the project
over to. Provide everything you feel would be relevant for them to ramp up quickly, such as tests, a README and instructions for how to run your project in a clean OSX/Linux environment.

# How to use it:
 1. Run `make install` command. It will create venv and install all necessary dependencies.
 2. Run `make run command='command'` to run the command with cron string as a single argument ('command'). For example, `make run command='*/15 0 1,15 * 1-5 /usr/bin/find'`3.
 3. Run `make test` to test the command.