import re

file_path = "templates/catalog/home.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Wrap V10 in comments
if "<!-- V10 HERO NEO-BENTO GRID START -->" in content and "{% comment %}\n<!-- V10 HERO NEO-BENTO GRID START -->" not in content:
    content = content.replace("<!-- V10 HERO NEO-BENTO GRID START -->", "{% comment %}\n<!-- V10 HERO NEO-BENTO GRID START -->")
    content = content.replace("<!-- V10 HERO NEO-BENTO GRID END -->", "<!-- V10 HERO NEO-BENTO GRID END -->\n{% endcomment %}")

# Prepare V11 (Modern E-commerce Full Width Store Style)
v11_html = """
<!-- V11 HERO E-COMMERCE MODERN START -->
<div class="relative w-full h-[65vh] md:h-[75vh] lg:h-[80vh] overflow-hidden group font-sans" x-data="heroSliderV11()" x-init="start()">

    <!-- Slides Container -->
    <div class="w-full h-full relative">
        <template x-for="(slide, index) in slides" :key="index">
            <div class="absolute inset-0 w-full h-full flex flex-col md:flex-row items-center justify-between px-6 md:px-16 lg:px-24"
                 x-show="active === index"
                 x-transition:enter="transition-all duration-[800ms] ease-[cubic-bezier(0.25,1,0.5,1)]"
                 x-transition:enter-start="opacity-0 translate-x-16"
                 x-transition:enter-end="opacity-100 translate-x-0"
                 x-transition:leave="transition-all duration-[600ms] ease-in-out z-0"
                 x-transition:leave-start="opacity-100 translate-x-0"
                 x-transition:leave-end="opacity-0 -translate-x-16">
                 
                 <!-- Background Color/Gradient tied to slide -->
                 <div class="absolute inset-0 -z-10 transition-colors duration-[1500ms]" :class="slide.bgColor"></div>
                 
                 <!-- Fine grain texture for modern premium feel -->
                 <div class="absolute inset-0 opacity-[0.02] mix-blend-overlay -z-10 pointer-events-none" style="background-image: url('data:image/svg+xml,%3Csvg viewBox=%220 0 200 200%22 xmlns=%22http://www.w3.org/2000/svg%22%3E%3Cfilter id=%22noise%22%3E%3CfeTurbulence type=%22fractalNoise%22 baseFrequency=%220.65%22 numOctaves=%223%22 stitchTiles=%22stitch%22/%3E%3C/filter%3E%3Crect width=%22100%25%22 height=%22100%25%22 filter=%22url(%23noise)%22/%3E%3C/svg%3E');"></div>

                 <!-- Splitted Content: Left Text -->
                 <div class="w-full md:w-1/2 flex flex-col justify-center z-10 pt-20 md:pt-0">
                     <span class="text-xs md:text-sm font-bold tracking-[0.25em] uppercase mb-4" 
                           :class="slide.textColor" 
                           x-text="slide.subtitle"
                           x-show="active === index"
                           x-transition:enter="transition-all duration-700 delay-300"
                           x-transition:enter-start="opacity-0 translate-y-4"
                           x-transition:enter-end="opacity-100 translate-y-0"></span>

                     <h2 class="text-5xl md:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.05] mb-6" 
                         :class="slide.titleColor" 
                         x-html="slide.title"
                         x-show="active === index"
                         x-transition:enter="transition-all duration-700 delay-500 ease-out"
                         x-transition:enter-start="opacity-0 translate-y-8"
                         x-transition:enter-end="opacity-100 translate-y-0"></h2>

                     <p class="text-lg md:text-xl font-medium max-w-lg mb-10 leading-relaxed" 
                        :class="slide.descColor" 
                        x-text="slide.description"
                        x-show="active === index"
                        x-transition:enter="transition-all duration-700 delay-700"
                        x-transition:enter-start="opacity-0 translate-y-8"
                        x-transition:enter-end="opacity-100 translate-y-0"></p>
                     
                     <div class="flex items-center gap-4"
                          x-show="active === index"
                          x-transition:enter="transition-all duration-700 delay-900"
                          x-transition:enter-start="opacity-0 translate-y-8"
                          x-transition:enter-end="opacity-100 translate-y-0">
                         <a :href="slide.link" class="px-10 py-5 rounded-xl font-bold uppercase tracking-widest text-[13px] transition-all duration-300 shadow-xl hover:-translate-y-1 hover:shadow-2xl flex items-center gap-3" :class="slide.btnClass">
                             <span x-text="slide.cta"></span>
                             <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                         </a>
                     </div>
                 </div>

                 <!-- Splitted Content: Right Image -->
                 <div class="w-full md:w-1/2 h-[45%] md:h-full flex items-center justify-center relative z-10 pb-10 md:pb-0">
                      <!-- Soft ambient glow behind product -->
                      <div class="absolute w-[70%] h-[70%] rounded-full blur-[100px] opacity-40 mix-blend-multiply" :class="slide.glowColor"></div>
                      
                      <img :src="slide.image" 
                           :alt="slide.title" 
                           class="relative z-10 w-[95%] lg:w-[110%] max-w-[650px] object-contain drop-shadow-[0_40px_40px_rgba(0,0,0,0.15)] transition-transform duration-[2000ms] ease-out hover:scale-[1.03]"
                           x-show="active === index"
                           x-transition:enter="transition-all duration-[1200ms] delay-500 ease-[cubic-bezier(0.25,1,0.5,1)]"
                           x-transition:enter-start="opacity-0 scale-90 translate-y-12"
                           x-transition:enter-end="opacity-100 scale-100 translate-y-0" />
                 </div>
            </div>
        </template>
    </div>

    <!-- Navigation Arrows -->
    <button @click="prev()" class="absolute left-4 top-1/2 transform -translate-y-1/2 w-12 h-12 rounded-full bg-white/70 backdrop-blur-md border border-gray-100 flex items-center justify-center text-gray-800 hover:bg-white transition-all opacity-0 group-hover:opacity-100 z-20 shadow-md hover:scale-105">
        <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
    </button>
    <button @click="next()" class="absolute right-4 top-1/2 transform -translate-y-1/2 w-12 h-12 rounded-full bg-white/70 backdrop-blur-md border border-gray-100 flex items-center justify-center text-gray-800 hover:bg-white transition-all opacity-0 group-hover:opacity-100 z-20 shadow-md hover:scale-105">
         <svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
    </button>

    <!-- Navigation Progress Indicator (Minimal Bar) -->
    <div class="absolute bottom-6 md:bottom-10 left-6 md:left-16 lg:left-24 flex items-center gap-2 md:gap-3 z-20 cursor-pointer">
        <template x-for="(slide, index) in slides" :key="index">
            <button @click="goTo(index)" class="group w-10 md:w-16 h-1.5 rounded-full overflow-hidden transition-all bg-gray-300/40 relative">
                <!-- Progress fill -->
                <div class="absolute inset-y-0 left-0 bg-gray-900 transition-all duration-75" x-show="active === index" :style="`width: ${progress}%`"></div>
                <!-- Hover effect -->
                <div class="absolute inset-0 bg-gray-400 opacity-0 group-hover:opacity-100 transition-opacity"></div>
            </button>
        </template>
    </div>
</div>
<!-- V11 HERO E-COMMERCE MODERN END -->
"""

# Insert V11 after V10
if "<!-- V11 HERO E-COMMERCE MODERN START -->" not in content:
    content = content.replace("<!-- V10 HERO NEO-BENTO GRID END -->\n{% endcomment %}", "<!-- V10 HERO NEO-BENTO GRID END -->\n{% endcomment %}\n\n" + v11_html)
else:
    print("V11 HERO is already in the file. Overwriting...")
    content = re.sub(r'<!-- V11 HERO E-COMMERCE MODERN START -->.*?<!-- V11 HERO E-COMMERCE MODERN END -->', v11_html, content, flags=re.DOTALL)

# Add heroSliderV11 script
v11_script = """
    function heroSliderV11() {
        return {
            active: 0,
            progress: 0,
            interval: null,
            progressInterval: null,
            slides: [
                {
                    subtitle: 'Destaque Absoluto',
                    title: 'Totem Triedro',
                    description: 'Atraia clientes de todos os lados com o Totem Triedro. Material extremamente leve, automontável e com impressão HD.',
                    image: "{% static 'img/totem_triedro.png' %}?v=17",
                    cta: 'COMPRAR AGORA',
                    link: '/produto/totem-triedro-em-poliondas/',
                    bgColor: 'bg-[#f0f4f8]',
                    textColor: 'text-blue-600',
                    titleColor: 'text-gray-900',
                    descColor: 'text-gray-600',
                    btnClass: 'bg-blue-600 text-white hover:bg-blue-700 shadow-blue-600/30',
                    glowColor: 'bg-blue-300'
                },
                {
                    subtitle: 'Lançamento',
                    title: 'Cubo Promo',
                    description: 'Construa vitrines criativas e ilhas sensacionais empilhando cubos super resistentes. Impacto visual imediato no PDV.',
                    image: "{% static 'img/cubo_ptbr.png' %}?v=12",
                    cta: 'COMPRAR AGORA',
                    link: '/produto/cubo-promocional-em-poliondas/',
                    bgColor: 'bg-[#fcf5ec]',
                    textColor: 'text-orange-600',
                    titleColor: 'text-gray-900',
                    descColor: 'text-gray-600',
                    btnClass: 'bg-orange-500 text-white hover:bg-orange-600 shadow-orange-500/30',
                    glowColor: 'bg-orange-300'
                },
                {
                    subtitle: 'Elegância Prática',
                    title: 'Banner Rollup',
                    description: 'Apresentação corporativa de luxo. Acompanha bolsa para transporte e é armado em menos de 10 segundos.',
                    image: "{% static 'img/rollup_hero.png' %}?v=10",
                    cta: 'COMPRAR AGORA',
                    link: '/produto/banner-rollup/',
                    bgColor: 'bg-[#f7f2fb]',
                    textColor: 'text-purple-600',
                    titleColor: 'text-gray-900',
                    descColor: 'text-gray-600',
                    btnClass: 'bg-purple-600 text-white hover:bg-purple-700 shadow-purple-600/30',
                    glowColor: 'bg-purple-300'
                }
            ],
            start() {
                this.resetInterval();
            },
            resetInterval() {
                clearInterval(this.interval);
                clearInterval(this.progressInterval);
                this.progress = 0;

                this.progressInterval = setInterval(() => {
                    this.progress += (100 / (6000 / 16)); 
                    if (this.progress > 100) this.progress = 100;
                }, 16);

                this.interval = setInterval(() => {
                    this.active = (this.active + 1) % this.slides.length;
                    this.resetInterval();
                }, 6000);
            },
            goTo(index) {
                this.active = index;
                this.resetInterval();
            },
            next() {
                this.active = (this.active + 1) % this.slides.length;
                this.resetInterval();
            },
            prev() {
                this.active = (this.active - 1 + this.slides.length) % this.slides.length;
                this.resetInterval();
            }
        }
    }
"""

if "function heroSliderV11()" not in content:
    content = content.replace("</script>", v11_script + "\n</script>", 1)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated home.html with V11 HERO (Modern E-Commerce Store Style) successfully!")
