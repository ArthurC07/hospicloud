
/**
* Theme: Montran Admin Template
* Author: Coderthemes
* Module/App: Main Js
 */

(function() {
  var changeptype, debounce, dh, dw, executeFunctionByName, h, initscrolls, resizeitems, toggle_fullscreen, toggle_slimscroll, w, wow;

  executeFunctionByName = function(functionName, context) {
    var args, func, i, namespaces;
    args = [].slice.call(arguments).splice(2);
    namespaces = functionName.split('.');
    func = namespaces.pop();
    i = 0;
    while (i < namespaces.length) {
      context = context[namespaces[i]];
      i++;
    }
    return context[func].apply(this, args);
  };

  resizeitems = function() {
    var i;
    if ($.isArray(resizefunc)) {
      i = 0;
      while (i < resizefunc.length) {
        window[resizefunc[i]]();
        i++;
      }
    }
  };

  initscrolls = function() {
    if (jQuery.browser.mobile !== true) {
      $('.slimscroller').slimscroll({
        height: 'auto',
        size: '5px'
      });
      $('.slimscrollleft').slimScroll({
        height: 'auto',
        position: 'right',
        size: '5px',
        color: '#7A868F',
        wheelStep: 5
      });
    }
  };

  toggle_slimscroll = function(item) {
    if ($('#wrapper').hasClass('enlarged')) {
      $(item).css('overflow', 'inherit').parent().css('overflow', 'inherit');
      $(item).siblings('.slimScrollBar').css('visibility', 'hidden');
    } else {
      $(item).css('overflow', 'hidden').parent().css('overflow', 'hidden');
      $(item).siblings('.slimScrollBar').css('visibility', 'visible');
    }
  };

  !(function($) {
    'use strict';
    var Sidemenu;
    Sidemenu = function() {
      this.$body = $('body');
      this.$openLeftBtn = $('.open-left');
      this.$menuItem = $('#sidebar-menu a');
    };
    return Sidemenu.prototype.openLeftBar = function() {
      $('#wrapper').toggleClass('enlarged');
      $('#wrapper').addClass('forced');
      if ($('#wrapper').hasClass('enlarged') && $('body').hasClass('fixed-left')) {
        $('body').removeClass('fixed-left').addClass('fixed-left-void');
      } else if (!$('#wrapper').hasClass('enlarged') && $('body').hasClass('fixed-left-void')) {
        $('body').removeClass('fixed-left-void').addClass('fixed-left');
      }
      if ($('#wrapper').hasClass('enlarged')) {
        $('.left ul').removeAttr('style');
      } else {
        $('.subdrop').siblings('ul:first').show();
      }
      toggle_slimscroll('.slimscrollleft');
      $('body').trigger('resize');
    };
  }, Sidemenu.prototype.menuItemClick = function(e) {
    if (!$('#wrapper').hasClass('enlarged')) {
      if ($(this).parent().hasClass('has_sub')) {
        e.preventDefault();
      }
      if (!$(this).hasClass('subdrop')) {
        $('ul', $(this).parents('ul:first')).slideUp(350);
        $('a', $(this).parents('ul:first')).removeClass('subdrop');
        $('#sidebar-menu .pull-right i').removeClass('md-remove').addClass('md-add');
        $(this).next('ul').slideDown(350);
        $(this).addClass('subdrop');
        $('.pull-right i', $(this).parents('.has_sub:last')).removeClass('md-add').addClass('md-remove');
        $('.pull-right i', $(this).siblings('ul')).removeClass('md-remove').addClass('md-add');
      } else if ($(this).hasClass('subdrop')) {
        $(this).removeClass('subdrop');
        $(this).next('ul').slideUp(350);
        $('.pull-right i', $(this).parent()).removeClass('md-remove').addClass('md-add');
      }
    }
  }, Sidemenu.prototype.init = function() {
    var $this;
    $this = this;
    $('.open-left').click(function(e) {
      e.stopPropagation();
      $this.openLeftBar();
    });
    $this.$menuItem.on('click', $this.menuItemClick);
    $('#sidebar-menu ul li.has_sub a.active').parents('li:last').children('a:first').addClass('active').trigger('click');
  }, $.Sidemenu = new Sidemenu, $.Sidemenu.Constructor = Sidemenu)(window.jQuery);

  (function($) {
    'use strict';
    var FullScreen;
    FullScreen = function() {
      this.$body = $('body');
      this.$fullscreenBtn = $('#btn-fullscreen');
    };
    return FullScreen.prototype.launchFullscreen = function(element) {
      if (element.requestFullscreen) {
        element.requestFullscreen();
      } else if (element.mozRequestFullScreen) {
        element.mozRequestFullScreen();
      } else if (element.webkitRequestFullscreen) {
        element.webkitRequestFullscreen();
      } else if (element.msRequestFullscreen) {
        element.msRequestFullscreen();
      }
    };
  }, FullScreen.prototype.exitFullscreen = function() {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.mozCancelFullScreen) {
      document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    }
  }, FullScreen.prototype.toggle_fullscreen = function() {
    var $this, fullscreenEnabled;
    $this = this;
    fullscreenEnabled = document.fullscreenEnabled || document.mozFullScreenEnabled || document.webkitFullscreenEnabled;
    if (fullscreenEnabled) {
      if (!document.fullscreenElement && !document.mozFullScreenElement && !document.webkitFullscreenElement && !document.msFullscreenElement) {
        $this.launchFullscreen(document.documentElement);
      } else {
        $this.exitFullscreen();
      }
    }
  }, FullScreen.prototype.init = function() {
    var $this;
    $this = this;
    $this.$fullscreenBtn.on('click', function() {
      $this.toggle_fullscreen();
    });
  }, $.FullScreen = new FullScreen, $.FullScreen.Constructor = FullScreen)(window.jQuery);

  (function($) {
    'use strict';

    /**
    Portlet Widget
     */
    var Portlet;
    Portlet = function() {
      this.$body = $('body');
      this.$portletIdentifier = '.portlet';
      this.$portletCloser = '.portlet a[data-toggle="remove"]';
      this.$portletRefresher = '.portlet a[data-toggle="reload"]';
    };
    return Portlet.prototype.init = function() {
      var $this;
      $this = this;
      $(document).on('click', this.$portletCloser, function(ev) {
        var $portlet, $portlet_parent;
        ev.preventDefault();
        $portlet = $(this).closest($this.$portletIdentifier);
        $portlet_parent = $portlet.parent();
        $portlet.remove();
        if ($portlet_parent.children().length === 0) {
          $portlet_parent.remove();
        }
      });
      $(document).on('click', this.$portletRefresher, function(ev) {
        var $pd, $portlet;
        ev.preventDefault();
        $portlet = $(this).closest($this.$portletIdentifier);
        $portlet.append('<div class="panel-disabled"><div class="loader-1"></div></div>');
        $pd = $portlet.find('.panel-disabled');
        setTimeout((function() {
          $pd.fadeOut('fast', function() {
            $pd.remove();
          });
        }), 500 + 300 * Math.random() * 5);
      });
    };
  }, $.Portlet = new Portlet, $.Portlet.Constructor = Portlet)(window.jQuery);

  (function($) {
    'use strict';
    var MoltranApp;
    MoltranApp = function() {
      this.VERSION = '1.1.0';
      this.AUTHOR = 'Coderthemes';
      this.SUPPORT = 'coderthemes@gmail.com';
      this.pageScrollElement = 'html, body';
      this.$body = $('body');
    };
    return MoltranApp.prototype.initTooltipPlugin = function() {
      $.fn.tooltip && $('[data-toggle="tooltip"]').tooltip();
    };
  }, MoltranApp.prototype.initPopoverPlugin = function() {
    $.fn.popover && $('[data-toggle="popover"]').popover();
  }, MoltranApp.prototype.initNiceScrollPlugin = function() {
    $.fn.niceScroll && $('.nicescroll').niceScroll({
      cursorcolor: '#9d9ea5',
      cursorborderradius: '0px'
    });
  }, MoltranApp.prototype.onDocReady = function(e) {
    FastClick.attach(document.body);
    resizefunc.push('initscrolls');
    resizefunc.push('changeptype');
    $('.animate-number').each(function() {
      $(this).animateNumbers($(this).attr('data-value'), true, parseInt($(this).attr('data-duration')));
    });
    $(window).resize(debounce(resizeitems, 100));
    $('body').trigger('resize');
    $('.right-bar-toggle').on('click', function(e) {
      e.preventDefault();
      $('#wrapper').toggleClass('right-bar-enabled');
    });
  }, MoltranApp.prototype.init = function() {
    var $this;
    $this = this;
    this.initTooltipPlugin();
    this.initPopoverPlugin();
    this.initNiceScrollPlugin();
    $(document).ready($this.onDocReady);
    $.Portlet.init();
    $.Sidemenu.init();
    $.FullScreen.init();
  }, $.MoltranApp = new MoltranApp, $.MoltranApp.Constructor = MoltranApp)(window.jQuery);

  (function($) {
    'use strict';
    $.MoltranApp.init();
  })(window.jQuery);


  /* ------------ some utility functions ----------------------- */

  toggle_fullscreen = function() {};

  w = void 0;

  h = void 0;

  dw = void 0;

  dh = void 0;

  changeptype = function() {
    w = $(window).width();
    h = $(window).height();
    dw = $(document).width();
    dh = $(document).height();
    if (jQuery.browser.mobile === true) {
      $('body').addClass('mobile').removeClass('fixed-left');
    }
    if (!$('#wrapper').hasClass('forced')) {
      if (w > 990) {
        $('body').removeClass('smallscreen').addClass('widescreen');
        $('#wrapper').removeClass('enlarged');
      } else {
        $('body').removeClass('widescreen').addClass('smallscreen');
        $('#wrapper').addClass('enlarged');
        $('.left ul').removeAttr('style');
      }
      if ($('#wrapper').hasClass('enlarged') && $('body').hasClass('fixed-left')) {
        $('body').removeClass('fixed-left').addClass('fixed-left-void');
      } else if (!$('#wrapper').hasClass('enlarged') && $('body').hasClass('fixed-left-void')) {
        $('body').removeClass('fixed-left-void').addClass('fixed-left');
      }
    }
    toggle_slimscroll('.slimscrollleft');
  };

  debounce = function(func, wait, immediate) {
    var result, timeout;
    timeout = void 0;
    result = void 0;
    return function() {
      var args, callNow, context, later;
      context = this;
      args = arguments;
      later = function() {
        timeout = null;
        if (!immediate) {
          result = func.apply(context, args);
        }
      };
      callNow = immediate && !timeout;
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
      if (callNow) {
        result = func.apply(context, args);
      }
      return result;
    };
  };

  wow = new WOW({
    boxClass: 'wow',
    animateClass: 'animated',
    offset: 50,
    mobile: false
  });

  wow.init();

}).call(this);
