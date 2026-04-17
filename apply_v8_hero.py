import re

file_path = "templates/catalog/home.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Wrap V7 in comments
content = content.replace("<!-- V7 HERO EDITORIAL SPLIT START -->", "{% comment %}\n<!-- V7 HERO EDITORIAL SPLIT START -->")
content = content.replace("<!-- V7 HERO EDITORIAL SPLIT END -->", "<!-- V7 HERO EDITORIAL SPLIT END -->\n{% endcomment %}")

# Prepare V8 (Opção 5 - Glazed Mesh / Apple Glass Style)
v8_html = """
<!-- V8 HERO GLAZED MESH START -->
<div class="relative w-full h-[85vh] lg:h-[95vh] flex items-center justify-center overflow-hidden bg-white" x-data="heroSliderV8()" x-init="start()">

    <!-- Fluid Mesh Gradient Background -->
    <div class="absolute inset-0 z-0 overflow-hidden pointer-events-none">
        
        <!-- Base light canvas -->
        <div class="absolute inset-0 bg-[#f8fafc]"></div>
        
        <!-- Smooth drifting color orbs -->
        <div class="absolute top-[-10%] left-[-10%] w-[50vw] h-[50vw] bg-pink-100 rounded-full mix-blend-multiply filter blur-[150px] opacity-70 animate-[pulse_10s_ease-in-out_infinite_reverse]"></div>
        <div class="absolute bottom-[-10%] right-[-10%] w-[60vw] h-[60vw] bg-blue-100 rounded-full mix-blend-multiply filter blur-[150px] opacity-70 animate-[pulse_12s_ease-in-out_infinite]"></div>
        <div class="absolute top-[20%] right-[20%] w-[40vw] h-[40vw] bg-purple-100 rounded-full mix-blend-multiply filter blur-[120px] opacity-50 animate-[pulse_8s_ease-in-out_infinite]"></div>
        
        <!-- Grid Pattern Overlay -->
        <div class="absolute inset-0 opacity-[0.03]" style="background-image: linear-gradient(to right, #000 1px, transparent 1px), linear-gradient(to bottom, #000 1px, transparent 1px); background-size: 40px 40px;"></div>
    </div>

    <!-- The Huge Glass Card Container -->
    <div class="container mx-auto px-4 relative z-20 h-full flex items-center max-w-7xl">
        <div class="w-full relative bg-white/40 backdrop-blur-3xl border border-white/60 shadow-[0_30px_60px_rgba(0,0,0,0.05)] rounded-[2.5rem] md:rounded-[3rem] px-8 py-12 md:p-16 lg:p-20 overflow-hidden h-[85%] flex flex-col justify-center">
            
            <template x-for="(slide, index) in slides" :key="index">
                <div class="absolute inset-0 w-full h-full p-8 md:p-16 lg:p-20"
                     x-show="active === index"
                     x-transition:enter="transition-all duration-[1000ms] ease-out"
                     x-transition:enter-start="opacity-0 scale-95"
                     x-transition:enter-end="opacity-100 scale-100"
                     x-transition:leave="transition-all duration-[600ms] ease-in"
                     x-transition:leave-start="opacity-100 scale-100"
                     x-transition:leave-end="opacity-0 scale-105">

                    <div class="flex flex-col lg:flex-row items-center h-full w-full gap-8 lg:gap-16">
                        
                        <!-- Left Content -->
                        <div class="lg:w-1/2 w-full flex flex-col justify-center z-20">
                            <!-- Premium Pill Badge -->
                            <div class="mb-6"
                                 x-show="active === index"
                                 x-transition:enter="transition-all duration-700 delay-300"
                                 x-transition:enter-start="opacity-0 -translate-y-4"
                                 x-transition:enter-end="opacity-100 translate-y-0">
                                <span class="inline-flex items-center gap-2 bg-white/80 rounded-full px-4 py-2 border border-white shadow-sm">
                                    <span class="w-2 h-2 rounded-full animate-pulse" :class="slide.badgeDotColor"></span>
                                    <span class="text-[10px] font-extrabold uppercase tracking-widest text-gray-700" x-text="slide.subtitle"></span>
                                </span>
                            </div>

                            <!-- Typography -->
                            <div class="mb-6"
                                 x-show="active === index"
                                 x-transition:enter="transition-all duration-[800ms] delay-500 ease-out"
                                 x-transition:enter-start="opacity-0 translate-y-8"
                                 x-transition:enter-end="opacity-100 translate-y-0">
                                <h2 class="text-5xl md:text-6xl lg:text-7xl font-extrabold leading-[1.1] tracking-tight text-gray-900 drop-shadow-sm" x-html="slide.title"></h2>
                            </div>

                            <div class="mb-10 max-w-md"
                                 x-show="active === index"
                                 x-transition:enter="transition-all duration-700 delay-700 ease-out"
                                 x-transition:enter-start="opacity-0 translate-y-8"
                                 x-transition:enter-end="opacity-100 translate-y-0">
                                <p class="text-lg md:text-xl text-gray-600 font-medium leading-relaxed drop-shadow-sm" x-text="slide.description"></p>
                            </div>

                            <!-- CTA Glass Button -->
                            <div class=""
                                 x-show="active === index"
                                 x-transition:enter="transition-all duration-700 delay-900 ease-out"
                                 x-transition:enter-start="opacity-0 translate-y-8"
                                 x-transition:enter-end="opacity-100 translate-y-0">
                                <a :href="slide.link" class="group relative px-8 py-4 bg-gray-900 text-white rounded-full overflow-hidden shadow-lg shadow-gray-900/20 hover:shadow-gray-900/40 transition-all duration-300 transform hover:-translate-y-1 inline-flex items-center gap-3">
                                    <span class="absolute inset-0 w-full h-full opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" :class="slide.buttonGradient"></span>
                                    <span class="relative font-bold tracking-wider uppercase text-xs z-10" x-text="slide.cta"></span>
                                    <svg class="w-4 h-4 transform group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform relative z-10" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
                                </a>
                            </div>
                        </div>

                        <!-- Right Image Content -->
                        <div class="lg:w-1/2 w-full h-[40vh] lg:h-full relative flex items-center justify-center z-10 perspective-1000">
                            <!-- Soft floor shadow under product -->
                            <div class="absolute bottom-[10%] w-[50%] h-[15px] bg-black/15 blur-xl rounded-[100%]"></div>
                            
                            <!-- Gentle Float Animation Frame -->
                            <div class="w-full h-full flex items-center justify-center animate-[floating_6s_ease-in-out_infinite]">
                                <img :src="slide.image"
                                     :alt="slide.title"
                                     class="relative z-10 w-[100%] max-w-[550px] object-contain drop-shadow-[0_20px_40px_rgba(0,0,0,0.15)]"
                                     x-show="active === index"
                                     x-transition:enter="transition-all duration-[1500ms] delay-500 ease-[cubic-bezier(0.34,1.56,0.64,1)]"
                                     x-transition:enter-start="opacity-0 scale-75 translate-x-16 rotate-[5deg]"
                                     x-transition:enter-end="opacity-100 scale-100 translate-x-0 rotate-0">
                            </div>
                        </div>
                    </div>
                </div>
            </template>

            <!-- Bottom Center Dots inside the glass card -->
            <div class="absolute bottom-8 lg:bottom-10 left-1/2 -translate-x-1/2 z-30 flex items-center gap-4 bg-white/50 backdrop-blur-md px-6 py-3 rounded-full border border-white/50 shadow-sm">
                <template x-for="(slide, idx) in slides" :key="idx">
                    <button @click="goTo(idx)" 
                            class="w-2.5 h-2.5 rounded-full transition-all duration-500 relative overflow-hidden ring-2 ring-transparent focus:outline-none"
                            :class="active === idx ? 'bg-gray-900 w-8 ring-offset-1' : 'bg-gray-400 hover:bg-gray-600'">
                        <div x-show="active === idx" class="absolute inset-x-0 h-full bg-white opacity-20" :style="`width: ${progress}%`"></div>
                    </button>
                </template>
            </div>
            
            <!-- Sleek Next/Prev internal buttons -->
            <button @click="prev()" class="absolute left-4 lg:left-8 top-1/2 -translate-y-1/2 w-10 h-10 bg-white/70 hover:bg-white text-gray-800 rounded-full flex items-center justify-center shadow-sm border border-white transition-all hover:scale-105 z-30">
                <svg class="w-4 h-4 mr-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
            </button>
            <button @click="next()" class="absolute right-4 lg:right-8 top-1/2 -translate-y-1/2 w-10 h-10 bg-white/70 hover:bg-white text-gray-800 rounded-full flex items-center justify-center shadow-sm border border-white transition-all hover:scale-105 z-30">
                <svg class="w-4 h-4 ml-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
            </button>

        </div>
    </div>
</div>

<style>
@keyframes floating {
    0% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-12px) rotate(1deg); }
    100% { transform: translateY(0px) rotate(0deg); }
}
</style>
<!-- V8 HERO GLAZED MESH END -->
"""
content = content.replace("<!-- V7 HERO EDITORIAL SPLIT END -->\n{% endcomment %}", "<!-- V7 HERO EDITORIAL SPLIT END -->\n{% endcomment %}\n\n" + v8_html)

# Add heroSliderV8 script
v8_script = """
    function heroSliderV8() {
        return {
            active: 0,
            progress: 0,
            interval: null,
            progressInterval: null,
            slides: [
                {
                    subtitle: 'Impacto Automontável',
                    title: 'Totem<br><span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">Triedro.</span>',
                    description: 'O material ideal para feiras intensas. Três faces de pura visibilidade, montagem em segundos e total flexibilidade.',
                    image: "{% static 'img/totem_triedro.png' %}?v=14",
                    cta: 'Personalizar',
                    link: '/produto/totem-triedro-em-poliondas/',
                    badgeDotColor: 'bg-blue-500',
                    buttonGradient: 'bg-gradient-to-r from-blue-600 to-indigo-600'
                },
                {
                    subtitle: 'Visibilidade Total',
                    title: 'Cubo<br><span class="text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-red-500">Promocional.</span>',
                    description: 'Geometria desenhada para as vitrines modernas. Construa ilhas gigantes com leveza.',
                    image: "{% static 'img/cubo_ptbr.png' %}?v=8",
                    cta: 'Configurar',
                    link: '/produto/cubo-promocional-em-poliondas/',
                    badgeDotColor: 'bg-orange-500',
                    buttonGradient: 'bg-gradient-to-r from-orange-500 to-red-500'
                },
                {
                    subtitle: 'Design Retrátil',
                    title: 'Banner<br><span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-pink-500">Rollup.</span>',
                    description: 'Sofisticação inquestionável para qualquer ambiente. Rollup elegante e estruturado.',
                    image: "{% static 'img/rollup_hero.png' %}?v=6",
                    cta: 'Reservar Agora',
                    link: '/produto/banner-rollup/',
                    badgeDotColor: 'bg-purple-500',
                    buttonGradient: 'bg-gradient-to-r from-purple-600 to-pink-500'
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
                    this.progress += (100 / (8000 / 16)); 
                    if (this.progress > 100) this.progress = 100;
                }, 16);

                this.interval = setInterval(() => {
                    this.active = (this.active + 1) % this.slides.length;
                    this.resetInterval();
                }, 8000);
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
content = content.replace("</script>", v8_script + "\n</script>")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated home.html with V8 HERO Glazed Mesh successfully!")
