import { IRenderMime } from '@jupyterlab/rendermime-interfaces';


import { JSONObject } from '@lumino/coreutils';


import { Widget } from '@lumino/widgets';

//import echarts from 'echarts/lib/echarts';
import * as echarts from 'echarts';


/**
 * The default mime type for the extension.
 */
const MIME_TYPE = 'application/vnd.yvis.v1+json';

/**
 * The class name added to the extension.
 */
const CLASS_NAME = 'mimerenderer-application/vnd.yvis.v1+json';

/**
 * A widget for rendering application/vnd.yvis.v1+json.
 */
export class OutputWidget extends Widget implements IRenderMime.IRenderer {
  /**
   * Construct a new output widget.
   */
  constructor(options: IRenderMime.IRendererOptions) {
    super();
    this._mimeType = options.mimeType;
    this.addClass(CLASS_NAME);
    this._div = document.createElement('div');
    this._width = '800px';
    this._height = '600px';
    this._div.setAttribute('style', `width: ${this._width}; height: ${this._height};`)
    this.node.appendChild(this._div)
    this._chart = undefined;
    this._option = {};
  }

  /**
   * Render application/vnd.yvis.v1+json into this widget's node.
   */
  renderModel(model: IRenderMime.IMimeModel): Promise<void> {
    
    let data = model.data[this._mimeType] as JSONObject;
    let meta: JSONObject = {};
    let scope: string = '';
    let theme: string = '';
    console.log(data)
    if (data.hasOwnProperty('meta') === true){
      meta = data.meta as JSONObject;
      if (meta.hasOwnProperty('scope') === true){
        if (meta.hasOwnProperty('height') === true && meta.hasOwnProperty('width') === true){
          if (meta.width !== this._width || meta.height !== this._height){
            this._height = meta.height as string
            this._width = meta.width as string
            this._div.setAttribute('style', `width: ${this._width}; height: ${this._height};`)
            if (this._chart !== undefined){
              this._chart.resize({height: this._height, width: this._width});
            }
          }
        }
        scope = meta.scope as string;
        if (scope === 'init' && this._chart === undefined){
          let initOptions: JSONObject = {};
          if (meta.hasOwnProperty('init') ===  true){
            initOptions = meta.init as JSONObject;
          }
          initOptions['height'] = this._height;
          initOptions['width'] = this._width;
          this._option = data.option as JSONObject;
          if (meta.hasOwnProperty('theme')){
            theme = meta.theme as string;
          }
          this._chart = echarts.init(this._div, theme, initOptions);
          this._chart.setOption(this._option);

        } else if (scope === 'update' && this._chart !== undefined){
          this._option = data.option as JSONObject;
          this._chart.setOption(this._option);
        } else if (scope === 'append' && this._chart !== undefined){
          let option: JSONObject = data.option as JSONObject;
          if (option.hasOwnProperty("dataset") === true){
              let dataset: Array<JSONObject> = option.dataset as Array<JSONObject> 
              dataset.forEach((element, idx) => {
                if (element.hasOwnProperty('source') === true){
                  let source: JSONObject = element.source as JSONObject;
                  Object.keys(source).forEach(colume => {
                    let _dataset: Array<JSONObject> = this._option.dataset as Array<JSONObject>
                    let _source: JSONObject = _dataset[idx].source as JSONObject;
                    let col: Array<any> = source[colume] as Array<any>
                    if (_source !== null){
                      let _col: Array<any> = _source[colume] as Array<any>;
                      if (_col !== null && _col !== undefined){
                        _col.push(...col);
                      }
                    }
                  })
                }
              })

          }
          this._chart.setOption(this._option);
        }
      }
    } else{
      console.log('Please provide meta content');
      this._div.textContent = JSON.stringify(data);
    }


    return Promise.resolve();
  }

  protected onResize(msg: Widget.ResizeMessage): void {
    if (this._chart !== undefined) {
      if (msg.height !== -1) {
        this._height = msg.height 
        this._width = msg.width 
        this._chart.resize({height: this._height, width: this._width});
      }
    }
  }  

  private _mimeType: string;
  private _div: HTMLDivElement;
  private _chart: echarts.ECharts | undefined;
  private _option: JSONObject;
  private _height: string | number;
  private _width: string | number;
}

/**
 * A mime renderer factory for application/vnd.yvis.v1+json data.
 */
export const rendererFactory: IRenderMime.IRendererFactory = {
  safe: true,
  mimeTypes: [MIME_TYPE],
  createRenderer: options => new OutputWidget(options)
};

/**
 * Extension definition.
 */
const extension: IRenderMime.IExtension = {
  id: 'yvis:plugin',
  rendererFactory,
  rank: 0,
  dataType: 'json',
  fileTypes: [
    {
      name: 'application/vnd.yvis.v1+json',
      mimeTypes: [MIME_TYPE],
      extensions: ['.yvis', '.yvis.json']
    }
  ],
  documentWidgetFactoryOptions: {
    name: 'JupyterLab yvis viewer',
    primaryFileType: 'application/vnd.yvis.v1+json',
    fileTypes: ['application/vnd.yvis.v1+json'],
    defaultFor: ['application/vnd.yvis.v1+json']
  }
};

export default extension;
