# adv-powerbi-js
Javascript implementation of Blender Uncertainty code in a Power BI Visual

Extending the [ADV-PowerBI](https://github.com/NewcastleRSE/ADV-PowerBI) project, reimplementing it using a full Power BI visual, coded in TypeScript rather than Python.

Project: Automating Data Visualisation (Turing)  
PI: [Nick Holliman](https://www.ncl.ac.uk/computing/people/profile/nickholliman.html)  
RSE(s): [Mike Simpson](https://www.ncl.ac.uk/digitalinstitute/staff/profile/mikesimpson.html)    

### Installing PowerBI Tools

Full instructions [here](https://docs.microsoft.com/en-gb/power-bi/developer/visuals/custom-visual-develop-tutorial)

### Testing the Visual
Using [Power BI Online](https://powerbi.microsoft.com/), go to Settings and enable Developer mode. Edit a report and add a Developer Visual to the report. Navigate to the visual's folder and run:

`pbiviz start`

Which will run the visual on your local computer and make it accessible through Power BI Onlien for testing.

### Compiling the Visual
Open PowerShell and navigate to the visual's folder. Then run:

`pbiviz package`

This will create a .pbiviz file in the dist folder, which can then be imported into Power BI Desktop.

### More Instructions
For more information (including diagrams, screenshots and examples), there is a full tutorial [Here](https://docs.microsoft.com/en-us/power-bi/developer/visuals/custom-visual-develop-tutorial). Part One includes testing instructions and Part Two contains compling instructions.
