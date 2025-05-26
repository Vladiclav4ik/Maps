L.ImageOverlay.Rotated = L.ImageOverlay.extend({
  initialize: function(image, topleft, topright, bottomleft, options) {
    if (typeof(image) === 'string') {
      this._url = image;
    } else {
      this._rawImage = image;
    }

    this._topLeft    = L.latLng(topleft);
    this._topRight   = L.latLng(topright);
    this._bottomLeft = L.latLng(bottomleft);

    L.setOptions(this, options);
  },

  onAdd: function(map) {
    if (!this._image) {
      this._initImage();

      if (this.options.opacity < 1) {
        this._updateOpacity();
      }
    }

    if (this.options.interactive) {
      L.DomUtil.addClass(this._rawImage, 'leaflet-interactive');
      this.addInteractiveTarget(this._rawImage);
    }

    map.on('zoomend resetview', this._reset, this);

    this.getPane().appendChild(this._image);
    this._reset();
  },

  onRemove: function(map) {
    map.off('zoomend resetview', this._reset, this);
    L.ImageOverlay.prototype.onRemove.call(this, map);
  },

  _initImage: function() {
    var img = this._rawImage;
    if (this._url) {
      img = L.DomUtil.create('img');
      img.style.display = 'none';

      if (this.options.crossOrigin) {
        img.crossOrigin = '';
      }

      img.src = this._url;
      this._rawImage = img;
    }
    L.DomUtil.addClass(img, 'leaflet-image-layer');

    var div = this._image = L.DomUtil.create('div', 'leaflet-image-layer ' + (this._zoomAnimated ? 'leaflet-zoom-animated' : ''));
    this._updateZIndex();
    div.appendChild(img);

    div.onselectstart = L.Util.falseFn;
    div.onmousemove = L.Util.falseFn;

    img.onload = function() {
      this._reset();
      img.style.display = 'block';
      this.fire('load');
    }.bind(this);

    img.alt = this.options.alt;
  },

  _reset: function() {
    var div = this._image;

    if (!this._map) {
      return;
    }

    var pxTopLeft    = this._map.latLngToLayerPoint(this._topLeft);
    var pxTopRight   = this._map.latLngToLayerPoint(this._topRight);
    var pxBottomLeft = this._map.latLngToLayerPoint(this._bottomLeft);

    var pxBounds = L.bounds([pxTopLeft, pxTopRight, pxBottomLeft]);
    var size = pxBounds.getSize();
    var pxTopLeftInDiv = pxTopLeft.subtract(pxBounds.min);

    this._bounds = L.latLngBounds(this._map.layerPointToLatLng(pxBounds.min), this._map.layerPointToLatLng(pxBounds.max));

    L.DomUtil.setPosition(div, pxBounds.min);
    div.style.width  = size.x + 'px';
    div.style.height = size.y + 'px';

    var imgW = this._rawImage.width;
    var imgH = this._rawImage.height;
    if (!imgW || !imgH) {
      return;
    }

    var vectorX = pxTopRight.subtract(pxTopLeft);
    var vectorY = pxBottomLeft.subtract(pxTopLeft);

    this._rawImage.style.transformOrigin = '0 0';

    this._rawImage.style.transform = "matrix(" +
      (vectorX.x/imgW) + ', ' + (vectorX.y/imgW) + ', ' +
      (vectorY.x/imgH) + ', ' + (vectorY.y/imgH) + ', ' +
      pxTopLeftInDiv.x + ', ' + pxTopLeftInDiv.y + ')';
  },

  reposition: function(topleft, topright, bottomleft) {
    this._topLeft    = L.latLng(topleft);
    this._topRight   = L.latLng(topright);
    this._bottomLeft = L.latLng(bottomleft);
    this._reset();
  },

  getTopLeft: function() {
    return this._topLeft;
  },

  getTopRight: function() {
    return this._topRight;
  },

  getBottomLeft: function() {
    return this._bottomLeft;
  },

  setUrl: function(url) {
    this._url = url;

    if (this._rawImage) {
      this._rawImage.src = url;
    }
    return this;
  }
}
);