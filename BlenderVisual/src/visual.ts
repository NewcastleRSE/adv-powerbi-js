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
    private container: Selection<SVGElement>;
    private circle: Selection<SVGElement>;
    private textValue: Selection<SVGElement>;
    private textLabel: Selection<SVGElement>;

    private visualSettings: VisualSettings;

    constructor(options: VisualConstructorOptions) {
        this.svg = d3.select(options.element)
            .append('svg')
            .classed('circleCard', true);
        this.container = this.svg.append("g")
            .classed('container', true);
        this.circle = this.container.append("circle")
            .classed('circle', true);
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

        let width: number = options.viewport.width;
        let height: number = options.viewport.height;

        let dataView: DataView = options.dataViews[0];

        // ------------------------- Set up JSON Data

        let doLog: boolean = true;

        if (doLog)
        {
            console.log("\nSettings:")
            console.log("visual: " + width + " x " + height);
            if (dataView.metadata.columns[0]) {console.log("x: " + dataView.metadata.columns[0].displayName);}
            if (dataView.metadata.columns[1]) {console.log("y: " + dataView.metadata.columns[1].displayName);}
            if (this.visualSettings) { console.log("m: " + this.visualSettings.visualDisplaySettings.displayMode); }
        }

        // CHECK DATA

        let dataCheck = true;

        if (!this.visualSettings) {         // visual settings not initialised (for some reason?)
            console.log("No VisualSettings Data");
            dataCheck = false;
        }
        if (!dataView.metadata.columns[0])
        {                                   // not supplied minumum dataset
            console.log("No Column 0");
            dataCheck = false;
        }
        if (!dataView.metadata.columns[1])
        {                                   // not supplied minumum dataset
            console.log("No Column 1");
            dataCheck = false;
        }
        if (!dataView.metadata.columns[2])
        {                                   // not supplied minumum dataset
            console.log("No Column 2");
            dataCheck = false;
        }
        if (!dataView.metadata.columns[3])
        {                                   // not supplied minumum dataset
            console.log("No Column 3");
            dataCheck = false;
        }

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

                console.log(json_data);
                JSON.stringify(json_data);
            }

            let valueString: string = "OK";
            let fontSizeValue: number = Math.min(width, height) / 6;
            this.textValue
                .text(valueString)
                .attr("x", "50%")
                .attr("y", "50%")
                .attr("dy", "0.2em")
                .attr("text-anchor", "middle")
                .style("font-size", fontSizeValue + "px");

            let fontSizeLabel: number = fontSizeValue / 3;
            this.textLabel
                .text("Data is Good!")
                .attr("x", "50%")
                .attr("y", height / 2)
                .attr("dy", fontSizeValue / 1.5)
                .attr("text-anchor", "middle")
                .style("font-size", fontSizeLabel + "px");
        }
        else 
        {
            let valueString: string = "ERROR";
            let fontSizeValue: number = Math.min(width, height) / 6;
            this.textValue
                .text(valueString)
                .attr("x", "50%")
                .attr("y", "50%")
                .attr("dy", "0.2em")
                .attr("text-anchor", "middle")
                .style("font-size", fontSizeValue + "px");

            let fontSizeLabel: number = fontSizeValue / 3;
            this.textLabel
                .text("Invalid Data")
                .attr("x", "50%")
                .attr("y", height / 2)
                .attr("dy", fontSizeValue / 1.5)
                .attr("text-anchor", "middle")
                .style("font-size", fontSizeLabel + "px");
        }

        // ---------------------------------------------------------------------- old circle code

        this.svg.attr("width", width);
        this.svg.attr("height", height);
        let radius: number = Math.min(width, height) / 2.2;

        this.visualSettings = VisualSettings.parse<VisualSettings>(dataView);

        this.visualSettings.circle.circleThickness = Math.max(0, this.visualSettings.circle.circleThickness);
        this.visualSettings.circle.circleThickness = Math.min(10, this.visualSettings.circle.circleThickness);

        this.circle
            .style("fill", this.visualSettings.circle.circleColor)
            .style("fill-opacity", 0.5)
            .style("stroke", "black")
            .style("stroke-width", this.visualSettings.circle.circleThickness)
            .attr("r", radius)
            .attr("cx", width / 2)
            .attr("cy", height / 2);
    }
}