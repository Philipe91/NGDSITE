document.addEventListener('DOMContentLoaded', function() {
  
  // Create Modal overlay
  const modalHTML = `
  <div id="cropper-modal" style="display:none; position:fixed; z-index:99999; left:0; top:0; width:100%; height:100%; background:rgba(0,0,0,0.8);">
      <div style="background:#fff; width:90%; height:90%; margin:2% auto; position:relative; overflow:hidden; border-radius:8px;">
          <h2 style="padding:10px 20px; background:#f4f4f4; margin:0; border-bottom:1px solid #ddd;">Cortar Imagem</h2>
          <div style="height: calc(100% - 100px); padding:20px;">
              <img id="cropper-image" src="" style="max-width:100%; max-height:100%;" />
          </div>
          <div style="position:absolute; bottom:0; left:0; right:0; padding:15px; background:#f4f4f4; border-top:1px solid #ddd; text-align:right;">
              <button type="button" id="cropper-cancel" style="padding:10px 20px; margin-right:10px; cursor:pointer;" class="button">Cancelar</button>
              <button type="button" id="cropper-save" style="padding:10px 20px; background:#417690; color:white; border:none; border-radius:4px; font-weight:bold; cursor:pointer;" class="button">Salvar Corte</button>
          </div>
      </div>
  </div>`;
  
  document.body.insertAdjacentHTML('beforeend', modalHTML);

  let cropper;
  let currentFileInput = null;
  let currentImgTag = null;
  
  const modal = document.getElementById('cropper-modal');
  const cropImage = document.getElementById('cropper-image');

  function openCropModal(fileInput, imgTag) {
      if(cropper) { cropper.destroy(); }
      currentFileInput = fileInput;
      currentImgTag = imgTag;
      
      // Load current image into cropper
      cropImage.src = imgTag.src;
      modal.style.display = 'block';

      // Small delay to ensure CSS calculations are ready
      setTimeout(() => {
          cropper = new Cropper(cropImage, {
              viewMode: 1,
              background: false,
              autoCropArea: 0.9,
          });
      }, 100);
  }

  document.getElementById('cropper-cancel').addEventListener('click', () => {
      modal.style.display = 'none';
      if(cropper) cropper.destroy();
  });

  document.getElementById('cropper-save').addEventListener('click', () => {
      if (!cropper) return;
      cropper.getCroppedCanvas({ imageSmoothingQuality: 'high' }).toBlob((blob) => {
          if(!blob) return;
          
          let fileName = "cropped_image.png";
          if(currentFileInput && currentFileInput.files && currentFileInput.files.length > 0) {
             fileName = currentFileInput.files[0].name;
          }
          
          const file = new File([blob], fileName, { type: 'image/png' });

          const dataTransfer = new DataTransfer();
          dataTransfer.items.add(file);
          
          currentFileInput.files = dataTransfer.files;
          currentImgTag.src = URL.createObjectURL(file);
          
          modal.style.display = 'none';
          cropper.destroy();
      }, 'image/png');
  });

  // Inject buttons into inline items
  function injectButtons() {
      const inlines = document.querySelectorAll('.inline-related');
      inlines.forEach((inline) => {
          if (!inline.classList.contains('empty-form') && inline.querySelector('img')) {
              if (inline.querySelector('.custom-crop-btn')) return; // Already exists
              
              const btn = document.createElement('button');
              btn.innerHTML = '✂️ Cortar';
              btn.className = 'custom-crop-btn button';
              btn.type = 'button'; // Do not submit form
              btn.style.cssText = 'position:absolute; top:5px; left:5px; z-index:900; background:#f5f5f5; border:1px solid #ccc; padding:2px 5px; border-radius:4px; font-size:12px; cursor:pointer; color:#333;';
              
              btn.addEventListener('click', function(e) {
                  e.preventDefault();
                  e.stopPropagation(); // prevent django-image-uploader from triggering file input click
                  
                  const fileInput = inline.querySelector('input[type="file"]');
                  const imgTag = inline.querySelector('img');
                  if(imgTag) {
                      openCropModal(fileInput, imgTag);
                  }
              });
              
              // Only insert if it has an image parent containing `.iuw-preview-icon` or similar container, or just attach to `.inline-related`
              inline.style.position = 'relative';
              inline.appendChild(btn);
          }
      });
  }

  // Observe DOM for new items added by Drag and Drop
  const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
          if(mutation.addedNodes.length > 0) {
              setTimeout(injectButtons, 100);
          }
      });
  });
  
  const rootGroup = document.querySelector('.inline-group');
  if(rootGroup) {
      observer.observe(rootGroup, { childList: true, subtree: true });
  }

  // Initial injection
  setTimeout(injectButtons, 500);

});
