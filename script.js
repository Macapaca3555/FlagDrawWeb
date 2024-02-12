


document.addEventListener("DOMContentLoaded", function() {

  canvas = document.getElementById('can');
  ctx = canvas.getContext("2d");
  const colourPicker = document.getElementById("colourpicker");
  const slider = document.getElementById("myRange");
  const colorButtons = document.querySelectorAll(".color-button");
  const clearbutton = document.querySelectorAll(".clear-button");
  const savebutton = document.querySelectorAll(".save-button");
  let isDrawing = false;
  canvas.addEventListener("mousedown", startDrawing);
  canvas.addEventListener("mouseup", stopDrawing);
  canvas.addEventListener("mousemove", draw);


  var colour = "black";
  var y = 2;
  var brushSize =2;
  colorButtons.forEach(button => {
                  button.addEventListener("click", () => {
                      const colour = button.style.backgroundColor;
                      const hexColour = rgbToHex(colour);
                      colourPicker.value = hexColour;
                  });
              });
  clearbutton.forEach(button => {
                  button.addEventListener("click", () => {
                        ctx.clearRect(0, 0, 500, 300);
                        document.getElementById("canvasimg").style.display = "none";
                    }
                  );
              });

 savebutton.forEach(button => {
                  button.addEventListener("click", () => {
                          save();
                        }
                      );
                  });
      function startDrawing(event) {
              isDrawing = true;
              draw(event); // Start drawing from the current mouse position
          }

      function stopDrawing() {
              isDrawing = false;
          }

      function draw(event) {
              if (!isDrawing) return;

              const x = event.offsetX;
              const y = event.offsetY;
              const colour = colourPicker.value;
              const brushSize = slider.value;
              ctx.fillStyle = colour;
              ctx.beginPath();
              ctx.arc(x, y, brushSize, 0, Math.PI * 2);
              ctx.fill();
          }
      function rgbToHex(rgb) {
                   // Convert rgb color to hexadecimal format
                   const match = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
                   if (!match) return rgb;
                   function hex(x) {
                       return ("0" + parseInt(x).toString(16)).slice(-2);
                   }
                   return "#" + hex(match[1]) + hex(match[2]) + hex(match[3]);
      }
      function save() {
          document.getElementById("canvasimg").style.border = "2px solid";
          var dataURL = canvas.toDataURL();
          document.getElementById("canvasimg").src = dataURL;
          document.getElementById("canvasimg").style.display = "inline";
      }
  });
