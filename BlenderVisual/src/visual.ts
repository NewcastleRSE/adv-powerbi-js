/*
*  Power BI Visual CLI
*
*  Copyright (c) Microsoft Corporation
*  All rights reserved.
*  MIT License
*
*  Permission is hereby granted, free of charge, to any person obtaining a copy
*  of this software and associated documentation files (the ""Software""), to deal
*  in the Software without restriction, including without limitation the rights
*  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
*  copies of the Software, and to permit persons to whom the Software is
*  furnished to do so, subject to the following conditions:
*
*  The above copyright notice and this permission notice shall be included in
*  all copies or substantial portions of the Software.
*
*  THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
*  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
*  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
*  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
*  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
*  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
*  THE SOFTWARE.
*/
"use strict";

import "core-js/stable";
import "./../style/visual.less";
import powerbi from "powerbi-visuals-api";
import VisualConstructorOptions = powerbi.extensibility.visual.VisualConstructorOptions;
import VisualUpdateOptions = powerbi.extensibility.visual.VisualUpdateOptions;
import IVisual = powerbi.extensibility.visual.IVisual;
import IVisualHost = powerbi.extensibility.IVisualHost;
import DataView = powerbi.DataView;
import EnumerateVisualObjectInstancesOptions = powerbi.EnumerateVisualObjectInstancesOptions;
import VisualObjectInstanceEnumeration = powerbi.VisualObjectInstanceEnumeration;

import { VisualSettings } from "./settings";

import * as d3 from "d3";
type Selection<T extends d3.BaseType> = d3.Selection<T, any, any, any>;

export class Visual implements IVisual {
    private host: IVisualHost;
    private svg: Selection<SVGElement>;
    private textValue: Selection<SVGElement>;
    private textLabel: Selection<SVGElement>;
    private container: Selection<SVGElement>;
    private visualSettings: VisualSettings;

    constructor(options: VisualConstructorOptions) {
        this.svg = d3.select(options.element)
            .append('svg');

        this.container = this.svg.append('svg')
        this.svg = this.container.append("image")
             .attr("xlink:href","https://turing-vis-blender.s3.eu-west-2.amazonaws.com/myImage.png")
             .attr("x", 0)
             .attr("y", 0);

        this.textValue = this.container.append("text")
             .classed("textValue", true);
        this.textLabel = this.container.append("text")
             .classed("textLabel", true);
    }

    public enumerateObjectInstances(options: EnumerateVisualObjectInstancesOptions): VisualObjectInstanceEnumeration {
        const settings: VisualSettings = this.visualSettings || <VisualSettings>VisualSettings.getDefault();
        return VisualSettings.enumerateObjectInstances(settings, options);
    }

    public update(options: VisualUpdateOptions) {

        let dataView: DataView = options.dataViews[0];
        this.visualSettings = VisualSettings.parse<VisualSettings>(dataView);

        let width: number = options.viewport.width;
        let height: number = options.viewport.height;

        // ------------------------- Set up JSON Data

        let doLog: boolean = false;

        if (doLog)
        {
            console.log("\nSettings:")
            console.log("visual: " + width + " x " + height);
            if (dataView.metadata.columns[0]) {console.log("x: " + dataView.metadata.columns[0].displayName);}
            if (dataView.metadata.columns[1]) {console.log("y: " + dataView.metadata.columns[1].displayName);}
            if (this.visualSettings) { console.log("m: " + this.visualSettings.visualDisplaySettings.displayMode); }
        }

        this.svg
            .attr("width",options.viewport.width)
            .attr("height",options.viewport.height);

        // CHECK DATA

        let dataCheck = true;

        if (!dataView.metadata.columns[3])  // not supplied minumum dataset
        {                                   
            //console.log("No Column " + 3);
            dataCheck = false;
        }

        let valueString: string = "OK";
        let labelString: string = "Data is Good!";

        if (dataCheck)
        {
            if (dataView.metadata.columns[0] && dataView.metadata.columns[1] && this.visualSettings)
            {
                // setup visualistion properties and settings
                let x_axis_label = dataView.metadata.columns[0].displayName;
                let y_axis_label = dataView.metadata.columns[1].displayName;
                
                if (this.visualSettings.dataDisplaySettings.xAxisLabel !== "") {
                    x_axis_label = this.visualSettings.dataDisplaySettings.xAxisLabel;
                }
                if (this.visualSettings.dataDisplaySettings.yAxisLabel !== "") {
                    y_axis_label = this.visualSettings.dataDisplaySettings.yAxisLabel;
                }

                let json_data = {
                    'key_name' : this.visualSettings.visualDisplaySettings.keyLabel,
                    'key_values' : { 
                        'high_value' : this.visualSettings.visualDisplaySettings.keyHighValue, 
                        'low_value' : this.visualSettings.visualDisplaySettings.keyLowValue 
                        },
                    'x_axis_label' : x_axis_label, 
                    'y_axis_label' : y_axis_label,
                    'background' : this.visualSettings.visualDisplaySettings.displayMode,
                    'data' : []
                }
                
                // populate visualisation data
                let idx = 0
                let numRows = dataView.table.rows.length;

                for (let x = 0; x < numRows; x++)
                {
                    let x_data = dataView.table.rows[idx][0];
                    let y_data = dataView.table.rows[idx][1];
                    let value_data = dataView.table.rows[idx][2];
                    let uncertainty_data = dataView.table.rows[idx][3];
                    let risk_data = dataView.table.rows[idx][4];

                    let j_data = { 'x': x_data, 'y': y_data, 'u': uncertainty_data, 'v': value_data }
                    
                    if (risk_data != null) {
                        j_data['r'] = risk_data;
                    }

                    json_data['data'].push(j_data);
                    
                    idx = idx + 1
                }

                //console.log(json_data);
                //JSON.stringify(json_data);
            }

            console.log("\nSending data good HTTPS request:")

            var request = new XMLHttpRequest()
            request.onload = function() 
            {
                console.log("YES Response:");
                console.log(this.response);
                d3.select("image")
                   .attr("xlink:href", this.response);
            }

            request.open('GET', 'https://automatingdatavisualisation.azurewebsites.net/datavistest?data=good', true)
            request.send()
        }
        else 
        {
            console.log("\nSending data bad HTTPS request:")

            var request = new XMLHttpRequest()
            request.onload = function() 
            {
                console.log("NO Response:");
                console.log(this.response);
                d3.select("image")
                    .attr("xlink:href", this.response);
            }
            request.open('GET', 'https://automatingdatavisualisation.azurewebsites.net/datavistest?data=bad', true)
            request.send()

            valueString = "ERROR";
            labelString = "Invalid Data"
        }

        let fontSizeValue: number = Math.min(width, height) / 6;
        this.textValue
            .text(valueString)
            .attr("x", "50%")
            .attr("y", "50%")
            .attr("dy", "0.2em")
            .attr("text-anchor", "middle")
            .style("font-size", fontSizeValue + "px")
            .style("stroke", "black")
            .style("fill", "white");

        let fontSizeLabel: number = fontSizeValue / 3;
        this.textLabel
            .text(labelString)
            .attr("x", "50%")
            .attr("y", height / 2)
            .attr("dy", fontSizeValue / 1.5)
            .attr("text-anchor", "middle")
            .style("font-size", fontSizeLabel + "px")
            .style("stroke", "black")
            .style("fill", "white");
    }
}