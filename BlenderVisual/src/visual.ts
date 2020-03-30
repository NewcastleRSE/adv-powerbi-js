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

    private svgRoot: Selection<SVGElement>;
    private svg: Selection<SVGElement>;
    private textValue: Selection<SVGElement>;
    private textLabel: Selection<SVGElement>;
    private container: Selection<SVGElement>;
    private visualSettings: VisualSettings;

    constructor(options: VisualConstructorOptions) {
        this.svgRoot = d3.select(options.element)
            .append('svg');

        this.container = this.svgRoot
            .append('svg');

        this.svg = this.container
            .append("image");

        this.textValue = this.container
            .append("text")
            .classed("textValue", true);
        
        this.textLabel = this.container
            .append("text")
            .classed("textLabel", true);
    }

    public enumerateObjectInstances(options: EnumerateVisualObjectInstancesOptions): VisualObjectInstanceEnumeration {
        const settings: VisualSettings = this.visualSettings || <VisualSettings>VisualSettings.getDefault();
        return VisualSettings.enumerateObjectInstances(settings, options);
    }

    public update(options: VisualUpdateOptions) {

        // parse dataView and visual settings
        let dataView: DataView = options.dataViews[0];
        this.visualSettings = VisualSettings.parse<VisualSettings>(dataView);

        // get viewport dimensions
        let width: number = options.viewport.width;
        let height: number = options.viewport.height;

        // ------------------------- Set up JSON Data

        let doLog: boolean = false;
        if (doLog) {
            console.log("\nSettings:")
            console.log("visual: " + width + " x " + height);
            if (dataView.metadata.columns[0]) { console.log("x: " + dataView.metadata.columns[0].displayName); }
            if (dataView.metadata.columns[1]) { console.log("y: " + dataView.metadata.columns[1].displayName); }
            if (this.visualSettings) { console.log("m: " + this.visualSettings.visualDisplaySettings.displayMode); }
        }

        // CHECK DATA                               -- Ensure that the minumum dataset has been provided
        let dataCheck = true;
        if (!dataView.metadata.columns[3])          // not supplied minumum dataset
        {
            //console.log("No Column " + 3);
            dataCheck = false;
        }

        let valueString: string = "";               // "Invalid Data" or "Please Wait"
        let labelString: string = "";               // Error message or "Render in Progress"

        if (dataCheck) {
            if (dataView.metadata.columns[0] && dataView.metadata.columns[1] && this.visualSettings) {
                // loop through columns to check that indexes are correct 
                let idx = 0;
                let numRows = dataView.table.rows.length;
                let numColumns = dataView.table.columns.length;

                let xIndex = 0, yIndex = 1, vIndex = 2, uIndex = 3, rIndex = 4;

                let x_axis_label = "";
                let y_axis_label = "";
                let key_value_name = "";
                let key_label = "";

                for (let x = 0; x < numColumns; x++) {
                    if (dataView.metadata.columns[x].roles.x === true) {
                        x_axis_label = dataView.metadata.columns[x].displayName
                        xIndex = x;
                    }
                    else if (dataView.metadata.columns[x].roles.y === true) {
                        y_axis_label = dataView.metadata.columns[x].displayName
                        yIndex = x;
                    }
                    else if (dataView.metadata.columns[x].roles.v === true) {
                        key_value_name = dataView.metadata.columns[x].displayName;
                        vIndex = x;
                    }
                    else if (dataView.metadata.columns[x].roles.u === true) {
                        key_label = dataView.metadata.columns[x].displayName;
                        uIndex = x;
                    }
                    else if (dataView.metadata.columns[x].roles.r === true) {
                        rIndex = x;
                    }
                }

                // check for user overrides
                if (this.visualSettings.dataDisplaySettings.xAxisLabel !== "") {
                    x_axis_label = this.visualSettings.dataDisplaySettings.xAxisLabel;
                }
                if (this.visualSettings.dataDisplaySettings.yAxisLabel !== "") {
                    y_axis_label = this.visualSettings.dataDisplaySettings.yAxisLabel;
                }
                if (this.visualSettings.visualDisplaySettings.valueKeyLabel !== "") {
                    key_value_name = this.visualSettings.visualDisplaySettings.valueKeyLabel;
                }
                if (this.visualSettings.visualDisplaySettings.valueKeyLabel !== "") {
                    key_label = this.visualSettings.visualDisplaySettings.keyLabel;
                }

                // setup visualistion properties and settings
                let json_data = {
                    'key_name': key_label,
                    'key_values': {
                        'high_value': this.visualSettings.visualDisplaySettings.keyHighValue,
                        'low_value': this.visualSettings.visualDisplaySettings.keyLowValue
                    },
                    'value_key_label': key_value_name,
                    'graph_settings': {
                        'background_colour': this.visualSettings.graphDisplaySettings.bgColour.substring(1, 7),
                        'label_colour': this.visualSettings.graphDisplaySettings.lblColour.substring(1, 7),
                        'text_colour': this.visualSettings.graphDisplaySettings.txtColour.substring(1, 7),
                        'gridline_colour': this.visualSettings.graphDisplaySettings.gridColour.substring(1, 7),
                        'axis_colour': this.visualSettings.graphDisplaySettings.axisColour.substring(1, 7),
                    },
                    'x_axis_label': x_axis_label,
                    'y_axis_label': y_axis_label,
                    'background': this.visualSettings.visualDisplaySettings.displayMode,
                    'data': []
                }

                // populate visualsiation data
                for (let x = 0; x < numRows; x++) {
                    let x_data = dataView.table.rows[idx][xIndex];
                    let y_data = dataView.table.rows[idx][yIndex];
                    let value_data = dataView.table.rows[idx][vIndex];
                    let uncertainty_data = dataView.table.rows[idx][uIndex];
                    let risk_data = dataView.table.rows[idx][rIndex];

                    let j_data = { 'x': x_data, 'y': y_data, 'u': uncertainty_data, 'v': value_data }

                    if (risk_data != null) {
                        j_data['r'] = risk_data;
                    }

                    json_data['data'].push(j_data);
                    idx = idx + 1
                }

                //console.log(json_data);
                let json_str = JSON.stringify(json_data);

                var request = new XMLHttpRequest()          // HTTP request, set image to response URL
                request.onload = function () {
                    d3.select("image")
                        .attr("xlink:href", this.response)
                        .attr("x", 0)
                        .attr("y", 0);
                    d3.selectAll("text")
                        .text("");
                }

                let callStr = 'https://automatingdatavisualisation.azurewebsites.net/datavistest?data=' + json_str;
                //console.log(callStr);

                request.open('POST', callStr, true)
                request.send()

                valueString = "";           // clear text
                labelString = "";
            }

            // clear image and display text
            d3.select("image")
                .attr("xlink:href", "");

            valueString = "PLEASE WAIT";
            labelString = "Render in Progress...";
        }
        else {
            // clear image and display text
            d3.select("image")
                .attr("xlink:href", "");

            valueString = "INVALID DATA";
            labelString = "Please provide x, y, value and uncertainty data.";
        }

        // render divs and text
        this.svgRoot
            .attr("width", width)
            .attr("height", height);

        this.svg
            .attr("width", width)
            .attr("height", height);

        this.container
            .attr("width", width)
            .attr("height", height);

        let fontSizeValue: number = Math.min(width, height) / 8;
        this.textValue
            .text(valueString)
            .attr("x", width / 2)
            .attr("y", height / 2)
            .attr("dy", "0.2em")
            .attr("text-anchor", "middle")
            .style("font-size", fontSizeValue + "px")
            .style("fill", "black");

        let fontSizeLabel: number = fontSizeValue / 3;
        this.textLabel
            .text(labelString)
            .attr("x", width / 2)
            .attr("y", height / 2)
            .attr("dy", fontSizeValue / 1.5)
            .attr("text-anchor", "middle")
            .style("font-size", fontSizeLabel + "px")
            .style("fill", "grey");
    }
}