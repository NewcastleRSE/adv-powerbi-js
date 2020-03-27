/*
 *  Power BI Visualizations
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

import { dataViewObjectsParser } from "powerbi-visuals-utils-dataviewutils";

export class VisualDisplaySettings {
  public displayMode: string = "graph";
  public keyType: string = "metTemp";
  public keyLabel: string = "Uncertainty";
  public keyHighValue: string = "Most Uncertain";
  public keyLowValue: string = "Least Uncertain";
  public valueKeyLabel: string = "";
}
export class DataDisplaySettings {
  public xAxisLabel: string = "";
  public yAxisLabel: string = "";
}
export class GraphDisplaySettings {
  public bgColour: string = "#D9D9D9";
  public lblColour: string = "#1A1A1A";
  public txtColour: string = "#1A1A1A";
  public gridColour: string = "#333333";
  public axisColour: string = "#000000";
}
export class VisualSettings extends dataViewObjectsParser.DataViewObjectsParser {
  public visualDisplaySettings: VisualDisplaySettings = new VisualDisplaySettings();
  public dataDisplaySettings: DataDisplaySettings = new DataDisplaySettings();
  public graphDisplaySettings: GraphDisplaySettings = new GraphDisplaySettings();
}
