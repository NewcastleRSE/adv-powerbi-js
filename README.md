# adv-powerbi-js
A javascript implementation of our Blender uncertainty visualisation code in a Power BI Custom Visual.

**Project:** Automating Data Visualisation (Turing)  
**PI:** [Nick Holliman](https://www.ncl.ac.uk/computing/people/profile/nickholliman.html)  
**RSE(s):** [Mike Simpson](https://www.ncl.ac.uk/digitalinstitute/staff/profile/mikesimpson.html)   

## About
This is an extension of the [ADV-PowerBI](https://github.com/NewcastleRSE/ADV-PowerBI) project, reimplemented using a full Power BI visual, coded in TypeScript rather than Python. 

The Visual runs inside the Power BI desktop application, which acts as a front end to the uncertainty visualisations. The Visual then calls out to Azure cloud resources, via an API and an Azure function, where all of the rendering etc. is executed. The resulting image is then downloaded back into the Visual. This allows the visual, which can use part of a 3D model of the city of Newcastle, to be used on low-powered devices such as phones or tablets.

## The Visual (Client)
The front-end of the application is the Visual, which can be imported into Power BI. To modify the visual's code, we recommend using VS Code and you will need to install Power BI tools and other dependencies, as described below.

### Installing PowerBI Tools
In order to develop and test the visual (see below) you need to install Power BI tools and the right certificates on your machine.
Full instructions [here](https://docs.microsoft.com/en-gb/power-bi/developer/visuals/custom-visual-develop-tutorial)

### Testing the Visual
When editing the visual, it is best to use 'Developer Mode'. Using [Power BI Online](https://powerbi.microsoft.com/), go to Settings and enable Developer mode. Edit a report and add a Developer Visual to the report. Navigate to the visual's folder and run:

`pbiviz start`

Which will run the visual on your local computer and make it accessible through Power BI Online for testing.

### Compiling the Visual
Open PowerShell and navigate to the visual's folder. Then run:

`pbiviz package`

This will create a .pbiviz file in the dist folder, which can then be imported into Power BI Desktop.

### More Instructions
For more information (including diagrams, screenshots and examples), there is a full tutorial [here](https://docs.microsoft.com/en-us/power-bi/developer/visuals/custom-visual-develop-tutorial). Part One includes testing instructions and Part Two contains compling instructions.

## The API (Server)
Then there is the API and the back-end code, which is currently configured to run on an Azure cloud node.

### The API
The api will need to be run on a webserver capable of running Blender. Just navigate to the API folder (i.e. in Powershell) and then type: 

`python .\api.py` 

This will start the API, which has a single, very simple endpoint. This calls out to Blender using the .blend file and .py scripts in the repository to render the image. 

Some settings relating to the lighting and the model are included in the Power BI file. Other properties are specified in the python scripts, but as much customisation has been enabled as possible using colour data and other options sent from the Power BI interface.

### Powershell Function
A Powershell function acts as a proxy between the visual and the api, allowing for HTTPS communication between the two entities. It is on the same virtual network as the Azure node and provides HTTPS access to the API, which is necessary for communication with The Visual.
