# Process

<!-- Same as assignment 1, same honesty. Which tools you used and for what; one
thing you kept and why it was good; one thing you rejected and why it was wrong.
"I did not use any" is fine if it is true.

If a model wrote most of plot.py, which is likely and allowed, the interesting part
is what you had to correct: did it invent a column name, use pandas where a list
would do, silently drop the rows it could not parse? -->

## Tools
I used VS Code to edit and run Python, Git to save changes, and Matplotlib to make the charts. I adapted the teacher's template with AI help for code and English wording. AI supplied much of the plotting code, which I added and ran step by step, checking the data and fixing errors with guidance.
## Kept
I kept the calendar heatmap and monthly bar chart because they show both daily changes and monthly totals. I also kept the orange highlights because they make the wettest day and month easy to find.

I checked the first five values printed by Python against the original JSON file before drawing the chart.
## Rejected
I replaced the template's CSV reader because my precipitation data was in JSON format.

During editing, I accidentally placed the figure creation code inside the monthly loop. This opened twelve windows, with the first eleven blank. With AI guidance, I moved that code outside the loop so the program created only one figure.