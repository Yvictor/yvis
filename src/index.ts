import { IRenderMime } from '@jupyterlab/rendermime-interfaces';


import { JSONObject } from '@lumino/coreutils';


import { Widget } from '@lumino/widgets';

/**
 * The default mime type for the extension.
 */
const MIME_TYPE = 'yvis+v1+json';

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
  }

  /**
   * Render application/vnd.yvis.v1+json into this widget's node.
   */
  renderModel(model: IRenderMime.IMimeModel): Promise<void> {
    
    let data = model.data[this._mimeType] as JSONObject;
    this.node.textContent = JSON.stringify(data);
    
    return Promise.resolve();
  }

  private _mimeType: string;
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
