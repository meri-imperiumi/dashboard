const epd = require('epd4in2');
const path = require('path');
const debug = require('debug')('signalk-epd:draw');

class Draw {
  constructor(config) {
    this.mode = null;
    this.expectedFlushTime = 0;
    this.values = {};
    this.drawing = false;
    this.setConfig(config);
  }

  setConfig(config) {
    this.displayFont = path.resolve(__dirname, './assets/nasalization-rg.ttf');
    this.bodyFont = path.resolve(__dirname, './assets/Eurostile.ttf');
    this.fontSizes = {
      mainLabel: 48,
      mainValue: 24,
      secondLabel: 24,
      secondValue: 12,
    };
    this.width = 400;
    this.height = 300;
    this.config = config;
  }

  setMode(mode) {
    if (this.mode === mode) {
      return;
    }
    debug(`Switching to display mode "${mode}"`);
    this.mode = mode;
    this.prepareDisplay();
  }

  getPaths() {
    return Object.keys(this.config[this.mode]);
  }

  updateValue(path, value, timestamp) {
    this.values[path] = {
      value,
      time: new Date(timestamp),
      rendered: false,
    };
  }

  prepareDisplay() {
    Object.keys(this.values).forEach((path) => {
      this.values[path].rendered = false;
    });
    this.drawFrame();
  }

  drawLabel(img) {
    const label = 'CURIOSITY'; // this.mode.toUpperCase();
    const labelBox = img.stringFTBBox(epd.colors.white, this.displayFont, this.fontSizes.mainLabel, 0, 0, 0, label);
    img.stringFT(epd.colors.white, this.displayFont, this.fontSizes.mainLabel, 0, 0,
      Math.round(epd.height - labelBox[1]), label);
  }

  drawFrame() {
    if (this.drawing) {
      debug('Still drawing a previous frame, abort');
      return Promise.resolve();
    }
    debug('Drawing frame');
    this.drawing = true;
    return epd.getImageBuffer('landscape')
      .then((img) => {
        this.drawLabel(img);
        img.negate();
        return epd.displayImageBuffer(img);
      })
      .then((res) => {
        debug('Drawing finished');
        this.drawing = false;
        return;
      });
  }

  init() {
    return epd.init();
  }

  clear() {
    return epd.clear();
  }

  sleep() {
    return epd.sleep();
  }
}

module.exports = Draw;
