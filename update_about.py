import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from apps.pages.models import Page

content = """
<div class="max-w-5xl mx-auto py-16 px-4 sm:px-6 lg:px-8 font-sans">
    <div class="text-center mb-16">
        <h2 class="text-4xl font-extrabold text-[#003366] sm:text-5xl uppercase tracking-tight">Quem Somos</h2>
        <div class="w-24 h-1 bg-secondary mx-auto mt-6 rounded-full"></div>
        <p class="mt-8 text-xl text-gray-500 max-w-3xl mx-auto leading-relaxed">
            A <strong>NGD - Núcleo Gráfico Digital</strong> é a referência B2B em Comunicação Visual e Impressão Digital em Brasília. Há mais de 18 anos nós transformamos grandes ideias em projetos palpáveis.
        </p>
    </div>

    <div class="space-y-16">
        <!-- Section: Nossa Historia -->
        <div class="flex flex-col md:flex-row items-center gap-12">
            <div class="md:w-1/2 group">
                <div class="relative overflow-hidden rounded-2xl shadow-xl bg-white border border-gray-100 p-8 flex items-center justify-center min-h-[300px] transition-all hover:border-primary/30">
                    <img src="/static/img/LOGO NGD.png" alt="NGD Núcleo Gráfico Digital" class="max-w-xs group-hover:scale-105 transition-transform duration-500" />
                </div>
            </div>
            <div class="md:w-1/2 space-y-6">
                <h3 class="text-3xl font-bold text-gray-900 tracking-tight">Nossa História</h3>
                <p class="text-gray-600 text-lg leading-relaxed">
                    Fundada em 2006, a NGD nasceu com a missão de entregar não apenas materiais impressos, mas sim uma <strong>solução completa</strong> em comunicação visual para o mercado corporativo. 
                </p>
                <p class="text-gray-600 text-lg leading-relaxed">
                    Com base sólida em processos industriais, nós dominamos a produção de painéis, estruturação de eventos com Box Truss, fabricação e montagem de Letras Caixa iluminadas e sinalização agrícola em grande escala.
                </p>
                <p class="text-gray-600 text-lg leading-relaxed">
                    No coração de Brasília, nosso parque gráfico integra impressão com tecnologia UV de secagem instantânea a plotters de recorte oscilante (CNC) de alta precisão. Se o mercado exige durabilidade e qualidade fotográfica, nossa indústria entrega.
                </p>
            </div>
        </div>

        <!-- Section: Especialidades -->
        <div class="bg-gradient-to-br from-surface to-[#f0f4f8] rounded-3xl p-10 lg:p-14 border border-gray-200">
            <h3 class="text-3xl font-bold text-center text-gray-900 mb-12">Nossas Especialidades</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                
                <!-- Card 1 -->
                <div class="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                    <div class="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center mb-6 text-primary">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
                    </div>
                    <h4 class="text-xl font-bold text-gray-900 mb-3">Sinalização Comercial</h4>
                    <p class="text-gray-600 leading-relaxed">Projetos estruturais completos para Fachadas em ACM, painéis corporativos, letra caixa e displays para PDV focados em conversão.</p>
                </div>

                <!-- Card 2 -->
                <div class="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                    <div class="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center mb-6 text-primary">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
                    </div>
                    <h4 class="text-xl font-bold text-gray-900 mb-3">Eventos e Congressos</h4>
                    <p class="text-gray-600 leading-relaxed">Aluguel, montagem e layoutização de Backdrops com Box Truss, portais de entrada, totens de orientação e pisos adesivados sob medida.</p>
                </div>

                <!-- Card 3 -->
                <div class="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 hover:shadow-lg hover:-translate-y-1 transition-all duration-300">
                    <div class="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center mb-6 text-primary">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
                    </div>
                    <h4 class="text-xl font-bold text-gray-900 mb-3">Tecnologia UV Absoluta</h4>
                    <p class="text-gray-600 leading-relaxed">Parque fabril equipado para impressão digital de altíssima definição em lona e materiais rígidos (Poliondas e Ps, Acrílico e MDF).</p>
                </div>

            </div>
        </div>
    </div>
</div>
"""

page, created = Page.objects.get_or_create(
    slug='sobre-nos',
    defaults={'title': 'Quem Somos - NGD', 'content': content, 'is_published': True}
)

if not created:
    page.title = "Quem Somos - NGD Núcleo Gráfico Digital"
    page.content = content
    page.save()

print("Page updated.")
