(function () {
  var hero = document.querySelector(".hero[data-hero-bg]");
  if (!hero) return;
  var canvas = hero.querySelector(".hero-canvas");
  if (!canvas) return;
  var ctx = canvas.getContext("2d");
  if (!ctx) return;

  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var width = hero.clientWidth || 1080;
  var height = hero.clientHeight || 380;
  var dpr = Math.min(window.devicePixelRatio || 1, 2);

  var hovering = false;
  var targetX = width * 0.68;
  var targetY = height * 0.42;
  var focusX = targetX;
  var focusY = targetY;
  var visible = true;
  var rafId = null;
  var time = 3.5;
  var nodes = [];

  function rand(seed) {
    var s = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
    return s - Math.floor(s);
  }

  function initNodes() {
    nodes.length = 0;
    var cols = Math.max(6, Math.min(13, Math.round(width / 105)));
    var rows = Math.max(4, Math.min(6, Math.round(height / 80)));
    var cellW = width / cols;
    var cellH = height / rows;

    for (var r = 0; r < rows; r++) {
      for (var c = 0; c < cols; c++) {
        var idx = r * cols + c + 1;
        var speed = 0.45;
        var angle = rand(idx * 31.7) * Math.PI * 2;
        var jitterX = (rand(idx * 4.3) - 0.5) * cellW * 0.65;
        var jitterY = (rand(idx * 9.1) - 0.5) * cellH * 0.65;
        nodes.push({
          x: (c + 0.5) * cellW + jitterX,
          y: (r + 0.5) * cellH + jitterY,
          vx: Math.cos(angle) * speed,
          vy: Math.sin(angle) * speed,
          size: 2 + rand(idx * 23.1) * 2.2,
          seed: rand(idx * 41.9)
        });
      }
    }
  }

  function resize() {
    var rect = hero.getBoundingClientRect();
    width = Math.max(rect.width, 300);
    height = Math.max(rect.height, 260);
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(width * dpr);
    canvas.height = Math.round(height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (!hovering) {
      targetX = width * 0.68;
      targetY = height * 0.42;
    }
    initNodes();
  }

  function updatePointer(clientX, clientY) {
    var rect = hero.getBoundingClientRect();
    var x = Math.max(0, Math.min(rect.width, clientX - rect.left));
    var y = Math.max(0, Math.min(rect.height, clientY - rect.top));
    targetX = x;
    targetY = y;
    hero.style.setProperty("--mouse-x", x.toFixed(1) + "px");
    hero.style.setProperty("--mouse-y", y.toFixed(1) + "px");
  }

  hero.addEventListener("mouseenter", function (e) {
    hovering = true;
    updatePointer(e.clientX, e.clientY);
  });
  hero.addEventListener("mousemove", function (e) {
    hovering = true;
    updatePointer(e.clientX, e.clientY);
  });
  hero.addEventListener("mouseleave", function () {
    hovering = false;
  });
  hero.addEventListener("touchmove", function (e) {
    if (e.touches.length > 0) {
      hovering = true;
      updatePointer(e.touches[0].clientX, e.touches[0].clientY);
    }
  }, { passive: true });
  hero.addEventListener("touchend", function () {
    hovering = false;
  });

  function drawConstellation() {
    var i, j, node, other, dx, dy, dist;
    var linkRadius = 140;
    var cursorRadius = 195;

    if (!reducedMotion) {
      for (i = 0; i < nodes.length; i++) {
        node = nodes[i];
        for (j = 0; j < nodes.length; j++) {
          if (i === j) continue;
          other = nodes[j];
          dx = node.x - other.x;
          dy = node.y - other.y;
          dist = Math.hypot(dx, dy) || 1;
          if (dist < 56) {
            var push = ((56 - dist) / 56) * 0.08;
            node.vx += (dx / dist) * push;
            node.vy += (dy / dist) * push;
          }
        }
        var spd = Math.hypot(node.vx, node.vy) || 1;
        if (spd > 0.65) {
          node.vx = (node.vx / spd) * 0.65;
          node.vy = (node.vy / spd) * 0.65;
        }
        node.x += node.vx;
        node.y += node.vy;

        if (node.x < 18) { node.x = 18; node.vx = Math.abs(node.vx); }
        else if (node.x > width - 18) { node.x = width - 18; node.vx = -Math.abs(node.vx); }
        if (node.y < 18) { node.y = 18; node.vy = Math.abs(node.vy); }
        else if (node.y > height - 18) { node.y = height - 18; node.vy = -Math.abs(node.vy); }
      }
    }

    for (i = 0; i < nodes.length; i++) {
      node = nodes[i];
      var distToFocus = Math.hypot(node.x - focusX, node.y - focusY);
      var boost = Math.max(0, 1 - distToFocus / cursorRadius);

      if (boost > 0.08) {
        ctx.strokeStyle = "#22d3ee";
        ctx.lineWidth = 1 + boost * 1.15;
        ctx.globalAlpha = boost * 0.48;
        ctx.beginPath();
        ctx.moveTo(focusX, focusY);
        ctx.lineTo(node.x, node.y);
        ctx.stroke();

        var pulseProgress = (time * 1.4 + node.seed * 3) % 1;
        var px = focusX + (node.x - focusX) * pulseProgress;
        var py = focusY + (node.y - focusY) * pulseProgress;
        ctx.fillStyle = "#a7f3d0";
        ctx.globalAlpha = boost * 0.9;
        ctx.beginPath();
        ctx.arc(px, py, 2.2, 0, Math.PI * 2);
        ctx.fill();
      }

      for (j = i + 1; j < nodes.length; j++) {
        other = nodes[j];
        var pairDist = Math.hypot(node.x - other.x, node.y - other.y);
        if (pairDist < linkRadius) {
          var alpha = (1 - pairDist / linkRadius) * (0.18 + boost * 0.55);
          ctx.strokeStyle = boost > 0.25 ? "#34d399" : "#10b981";
          ctx.lineWidth = 1;
          ctx.globalAlpha = alpha;
          ctx.beginPath();
          ctx.moveTo(node.x, node.y);
          ctx.lineTo(other.x, other.y);
          ctx.stroke();
        }
      }
    }

    for (i = 0; i < nodes.length; i++) {
      node = nodes[i];
      var dFocus = Math.hypot(node.x - focusX, node.y - focusY);
      var b = Math.max(0, 1 - dFocus / cursorRadius);
      ctx.fillStyle = b > 0.35 ? "#6ee7b7" : "#10b981";
      ctx.globalAlpha = 0.4 + b * 0.6;
      ctx.beginPath();
      ctx.arc(node.x, node.y, node.size + b * 2.2, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  function frame() {
    if (!visible) {
      rafId = null;
      return;
    }
    if (!reducedMotion) {
      time += 0.016;
    }
    if (!hovering && !reducedMotion) {
      targetX = width * 0.64 + Math.cos(time * 0.65) * (width * 0.22);
      targetY = height * 0.46 + Math.sin(time * 0.9) * (height * 0.22);
      hero.style.setProperty("--mouse-x", targetX.toFixed(1) + "px");
      hero.style.setProperty("--mouse-y", targetY.toFixed(1) + "px");
    }
    focusX += (targetX - focusX) * (hovering ? 0.16 : 0.06);
    focusY += (targetY - focusY) * (hovering ? 0.16 : 0.06);

    ctx.clearRect(0, 0, width, height);
    drawConstellation();

    if (!reducedMotion) {
      rafId = requestAnimationFrame(frame);
    }
  }

  resize();

  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        visible = entry.isIntersecting;
        if (visible && rafId === null) {
          frame();
        } else if (!visible && rafId !== null) {
          cancelAnimationFrame(rafId);
          rafId = null;
        }
      });
    }, { rootMargin: "150px 0px" }).observe(hero);
  }

  if ("ResizeObserver" in window) {
    new ResizeObserver(function () {
      resize();
      if (reducedMotion) frame();
    }).observe(hero);
  } else {
    window.addEventListener("resize", resize);
  }

  frame();
})();
