import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight, Maximize2, Minimize2 } from 'lucide-react';

// --- Types ---
type SlideContent = {
  id: number;
  type: 'title' | 'index' | 'content' | 'profile' | 'profile-detail' | 'quote' | 'image-grid';
  title?: string;
  subtitle?: string;
  body?: string;
  highlight?: string;
  items?: string[];
  links?: { text: string; url: string }[];
  imageAlt?: string;
};

// --- Data (Updated to match the source exactly) ---
const slides: SlideContent[] = [
  {
    id: 1,
    type: 'title',
    title: 'XR CONCERT',
    subtitle: 'Unreal Engine Project'
  },
  {
    id: 2,
    type: 'index',
    title: 'INDEX',
    items: ['1. Purpose', '2. Project Strategy', '3. Artist', '4. Levels']
  },
  {
    id: 3,
    type: 'content',
    title: 'PURPOSE',
    subtitle: '언리얼엔진으로 구현하는 XR콘서트의 목적',
    body: '언리얼엔진은 사진처럼 사실적인 고품질 그래픽을 실시간으로 구현할 수 있는 게임 엔진 프로그램이다. 따라서 XR콘서트에서 언리얼엔진을 사용하는 목적과 이유는 사실적인 공간을 재현하는 무대를 구성하며, 현실과 가상을 넘나들기 위함일 것이다.',
    highlight: '그렇다면 언리얼 환경에서 단상이 있는 XR 콘서트를 구현할 필요가 있는가?',
  },
  {
    id: 4,
    type: 'content',
    title: '첫번째',
    body: "리얼 타임으로 구현을 한다고 가정을 했을 때, 현재는 ICVFX, 즉 IN-Camera VFX 방식을 사용한 콘서트가 대다수이다 (이마저도 유튜브에 'XR콘서트'라고 검색어를 치면 참고할만한 자료가 3년 전.). 근데 이 ICVFX 스튜디오는 이미 LED 스크린으로 구성된 바닥과 벽이 이미 단상처럼 구성되어있다. 심지어 메인 조명도 언리얼 환경이 아닌 실제 환경에서 컨트롤 한다.",
    highlight: "'X'라고 생각한다. 그 이유는 크게 두가지가 있다."
  },
  {
    id: 5,
    type: 'content',
    title: '두번째',
    body: "XR콘서트의 콘텐츠를 제공할 때, 대부분의 소비자들은 헤드마운트와 같은 기기를 사용할 것이다. 이를 보았을 때, 콘텐츠를 소비하는 사람들은 '과연 현실에 있는 무대를 원할까?' 아니면 '현실에서 느낄 수 없는 다른 차원의 것을 원할까?' 이를 고민해보았을 때, 역시나 후자가 더 많을 것이다.",
    highlight: "현실에서 느낄 수 없는 다른 차원의 것을 원할까?"
  },
  {
    id: 6,
    type: 'content',
    title: 'PROJECT STRATEGY',
    body: '그렇기 때문에, 현실에서 만들어낼 수 없는 (혹은 실제 환경에서 표현하기 어려운) 요소와 구성을 넣는 것이 필요하다고 생각했다.',
    links: [
      { text: '참고 자료 보기 →', url: 'https://www.instagram.com/p/DFCkAR1ytkA/' },
      { text: 'Rolling Stone Korea 기사 보기 →', url: 'https://rollingstone.co.kr/main/$/21209' }
    ],
    highlight: '그래서 프로젝트 안에 여러 개의 컨셉적인 테마를 가진 각각의 레벨을 제작을 하였다. 이는 하나의 스튜디오에 여러개의 세트장이 있는 효과를 낼 수 있다.'
  },
  {
    id: 7,
    type: 'profile',
    title: 'ARTIST',
    subtitle: '아티스트 소개 및 콘서트 로그라인',
    body: '아티스트에 대한 조사를 한 뒤, 아티스트의 컨셉과 어울리는 콘서트 제작을 계획하였다.',
    highlight: '아티스트 소개'
  },
  {
    id: 8,
    type: 'profile-detail',
    title: '딘(Dean)',
    items: [
      'GENRE: Alternative RnB, Future RnB',
      'CONCEPT: Distopia / 신비주의 / 도시적인 / 몽환 <1984>',
      '그 외 특징: 인스타 계정 이름도 뒤에 trbl(Trouble)을 붙이며, 특유의 우울함을 추구'
    ],
    links: [
        { text: 'Instagram 프로필 보기 →', url: 'https://www.instagram.com/deantrbl/' }
    ]
  },
  {
    id: 9,
    type: 'quote',
    title: '콘서트 로그라인',
    highlight: '"무너져가는 디스토피아에서 불안정함을 노래하다."'
  },
  {
    id: 10,
    type: 'image-grid',
    title: '4. Levels',
    body: '노래에 어울리는 컨셉과 관련된 내용으로 레벨을 제작하였다.',
    items: ['Howlin\' 404', 'NASA', 'Bonnie & Clyde', 'Nocturne 07']
  }
];

// --- Components ---

const SlideContainer = ({ children }: { children: React.ReactNode }) => (
  <div className="w-full h-full flex flex-col justify-center items-start p-8 md:p-16 text-left relative overflow-hidden">
    {children}
  </div>
);

const TitleSlide = ({ title, subtitle }: { title?: string, subtitle?: string }) => (
  <SlideContainer>
    <div className="absolute inset-0 bg-[#050505] z-0" />
    <div className="z-10 relative w-full flex flex-col items-center justify-center">
      {/* Glitch effect wrapper */}
      <div className="relative inline-block">
        {/* Main title - white */}
        <h1 className="text-6xl md:text-8xl font-black tracking-tighter text-white mb-4 drop-shadow-2xl relative z-3 uppercase" style={{ fontFamily: "'Archivo Black', sans-serif" }}>
          {title}
        </h1>
        {/* Glitch layer 1 - green */}
        <h1 className="absolute top-0 left-0 text-6xl md:text-8xl font-black tracking-tighter text-[#CCFF00] mb-4 drop-shadow-2xl z-1 opacity-90 uppercase pointer-events-none" style={{ fontFamily: "'Archivo Black', sans-serif", transform: 'translate3d(-4px, 0, 0)', mixBlendMode: 'screen' }}>
          {title}
        </h1>
        {/* Glitch layer 2 - red */}
        <h1 className="absolute top-0 left-0 text-6xl md:text-8xl font-black tracking-tighter text-[#ff3b3b] mb-4 drop-shadow-2xl z-2 opacity-90 uppercase pointer-events-none" style={{ fontFamily: "'Archivo Black', sans-serif", transform: 'translate3d(4px, 0, 0)', mixBlendMode: 'screen' }}>
          {title}
        </h1>
      </div>
      <h2 className="text-2xl md:text-3xl font-light text-white mt-6" style={{ fontFamily: "'Inter', sans-serif", letterSpacing: '0.05em' }}>
        {subtitle}
      </h2>
    </div>
  </SlideContainer>
);

const IndexSlide = ({ items }: { items?: string[] }) => (
  <SlideContainer>
    <div className="absolute inset-0 bg-[#050505] z-0" />
    {/* Background XR CONCERT text */}
    <div className="absolute inset-0 flex items-center justify-center z-0 pointer-events-none">
      <span className="text-[120px] font-black text-white opacity-5 uppercase tracking-wider" style={{ fontFamily: "'Archivo Black', sans-serif" }}>
        XR CONCERT
      </span>
    </div>
    <div className="z-10 relative w-full">
      <ul className="space-y-6 flex flex-col items-center">
        {items?.map((item, idx) => (
          <li key={idx} className="text-3xl md:text-4xl font-black text-white transition-colors cursor-default" style={{ fontFamily: "'Archivo Black', sans-serif" }}>
            {item}
          </li>
        ))}
      </ul>
    </div>
  </SlideContainer>
);

const ContentSlide = ({ title, subtitle, body, highlight, items, links }: { title?: string, subtitle?: string, body?: string, highlight?: string, items?: string[], links?: { text: string; url: string }[] }) => (
  <SlideContainer>
    <div className="absolute inset-0 bg-[#050505] z-0" />
    <div className="z-10 relative w-full max-w-5xl">
      {/* Glassmorphism container */}
      <div className="bg-white/2 backdrop-blur-[20px] border border-white/8 rounded-3xl p-12 shadow-[0_8px_32px_rgba(0,0,0,0.1)]" style={{ backdropFilter: 'blur(20px) saturate(180%)' }}>
        <h2 className="text-4xl md:text-5xl font-black text-[#CCFF00] mb-4 uppercase tracking-wider" style={{ fontFamily: "'Archivo Black', sans-serif", textShadow: '0 0 30px rgba(204,255,0,0.4)' }}>
          {title}
        </h2>

        {subtitle && (
            <h3 className="text-xl md:text-2xl font-medium text-white mb-8" style={{ fontFamily: "'Inter', sans-serif" }}>
                {subtitle}
            </h3>
        )}
        
        {body && (
          <p className="text-lg md:text-xl text-white leading-relaxed mb-8 whitespace-pre-wrap opacity-95" style={{ fontFamily: "'Inter', sans-serif" }}>
            {body}
          </p>
        )}

        {items && (
          <ul className="space-y-4 mb-8">
            {items.map((item, idx) => (
              <li key={idx} className="text-lg md:text-xl text-white border-l-4 border-white/20 pl-4" style={{ fontFamily: "'Inter', sans-serif" }}>
                {item}
              </li>
            ))}
          </ul>
        )}

        {links && (
          <div className="flex flex-col gap-3 mb-8">
            {links.map((link, idx) => (
              <a key={idx} href={link.url} target="_blank" rel="noopener noreferrer" className="text-[#CCFF00] hover:text-white transition-colors flex items-center gap-2 font-bold text-lg hover:underline" style={{ fontFamily: "'Inter', sans-serif" }}>
                {link.text}
              </a>
            ))}
          </div>
        )}

        {highlight && (
          <div className="mt-auto w-full bg-[#CCFF00]/3 backdrop-blur-[10px] border border-[#CCFF00]/30 p-6 rounded-2xl border-l-4 border-l-[#CCFF00]">
            <p className="text-xl md:text-2xl font-semibold text-[#CCFF00] italic text-center" style={{ fontFamily: "'Inter', sans-serif" }}>
              {highlight}
            </p>
          </div>
        )}
      </div>
    </div>
  </SlideContainer>
);

const QuoteSlide = ({ highlight, title }: { highlight?: string, title?: string }) => (
  <SlideContainer>
    <div className="absolute inset-0 bg-[#050505] z-0" />
    <div className="z-10 relative w-full flex flex-col items-center justify-center">
      {/* Glassmorphism container */}
      <div className="bg-white/2 backdrop-blur-[20px] border border-white/8 rounded-3xl p-12 shadow-[0_8px_32px_rgba(0,0,0,0.1)] max-w-4xl" style={{ backdropFilter: 'blur(20px) saturate(180%)' }}>
        {title && (
          <p className="text-sm text-white/50 tracking-[0.3em] uppercase mb-8 text-center" style={{ fontFamily: "'Inter', sans-serif" }}>
            {title}
          </p>
        )}
        <h2 className="text-3xl md:text-5xl font-bold text-[#CCFF00] leading-tight text-center" style={{ fontFamily: "'Inter', sans-serif" }}>
          {highlight}
        </h2>
      </div>
    </div>
  </SlideContainer>
);

const ProfileSlide = ({ title, subtitle, body, highlight }: { title?: string, subtitle?: string, body?: string, highlight?: string }) => (
  <SlideContainer>
    <div className="absolute inset-0 bg-[#050505] z-0" />
    <div className="z-10 relative w-full max-w-5xl">
      {/* Glassmorphism container */}
      <div className="bg-white/2 backdrop-blur-[20px] border border-white/8 rounded-3xl p-12 shadow-[0_8px_32px_rgba(0,0,0,0.1)]" style={{ backdropFilter: 'blur(20px) saturate(180%)' }}>
        <h2 className="text-4xl md:text-5xl font-black text-[#CCFF00] mb-4 uppercase tracking-wider" style={{ fontFamily: "'Archivo Black', sans-serif", textShadow: '0 0 30px rgba(204,255,0,0.4)' }}>
          {title}
        </h2>

        {subtitle && (
            <h3 className="text-xl md:text-2xl font-medium text-white mb-8" style={{ fontFamily: "'Inter', sans-serif" }}>
                {subtitle}
            </h3>
        )}
        
        {body && (
          <p className="text-lg md:text-xl text-white leading-relaxed mb-8 whitespace-pre-wrap opacity-95" style={{ fontFamily: "'Inter', sans-serif" }}>
            {body}
          </p>
        )}

        {highlight && (
          <div className="text-xl md:text-2xl font-semibold text-[#CCFF00] mb-8" style={{ fontFamily: "'Inter', sans-serif" }}>
            {highlight}
          </div>
        )}
      </div>
    </div>
  </SlideContainer>
);

const ProfileDetailSlide = ({ title, items, links }: { title?: string, items?: string[], links?: { text: string; url: string }[] }) => (
  <SlideContainer>
    <div className="absolute inset-0 bg-[#050505] z-0" />
    <div className="z-10 relative w-full max-w-5xl">
      {/* Glassmorphism container */}
      <div className="bg-white/2 backdrop-blur-[20px] border border-white/8 rounded-3xl p-12 shadow-[0_8px_32px_rgba(0,0,0,0.1)]" style={{ backdropFilter: 'blur(20px) saturate(180%)' }}>
        {/* Profile Image */}
        <div className="flex flex-col items-center mb-8">
          <img 
            src="deantrbl-profile.webp" 
            alt="딘(Dean) 프로필"
            className="w-48 h-48 rounded-full object-cover border-4 border-[#CCFF00]/30 shadow-[0_8px_32px_rgba(0,0,0,0.4)] mb-4"
            onError={(e) => {
              const target = e.target as HTMLImageElement;
              target.style.display = 'none';
            }}
          />
          <h2 className="text-3xl md:text-4xl font-bold text-[#CCFF00] mb-4" style={{ fontFamily: "'Archivo Black', sans-serif", textShadow: '0 0 20px rgba(204,255,0,0.4)' }}>
            {title}
          </h2>
        </div>

        {items && (
          <div className="space-y-6 mb-8">
            {items.map((item, idx) => {
              const [label, ...valueParts] = item.split(': ');
              const value = valueParts.join(': ');
              return (
                <div key={idx} className="border-b border-white/6 pb-4">
                  <div className="text-sm text-white/50 uppercase tracking-wider mb-2" style={{ fontFamily: "'Inter', sans-serif" }}>
                    {label}
                  </div>
                  <div className="text-lg md:text-xl text-white" style={{ fontFamily: "'Inter', sans-serif" }}>
                    {value}
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {links && (
          <div className="flex flex-col gap-3">
            {links.map((link, idx) => (
              <a key={idx} href={link.url} target="_blank" rel="noopener noreferrer" className="text-[#CCFF00] hover:text-white transition-colors flex items-center gap-2 font-bold text-lg hover:underline" style={{ fontFamily: "'Inter', sans-serif" }}>
                {link.text}
              </a>
            ))}
          </div>
        )}
      </div>
    </div>
  </SlideContainer>
);

const ImageGridSlide = ({ title, body, items }: { title?: string, body?: string, items?: string[] }) => {
  const projectImages = [
    'project-strategy-1.jpeg',
    'project-strategy-2.jpeg',
    'project-strategy-3.jpeg',
    'project-strategy-4.jpeg',
    'project-strategy-5.jpeg'
  ];

  return (
    <SlideContainer>
      <div className="absolute inset-0 bg-[#050505] z-0" />
      <div className="z-10 relative w-full h-full flex flex-col">
        {/* Glassmorphism container */}
        <div className="bg-white/2 backdrop-blur-[20px] border border-white/8 rounded-3xl p-12 shadow-[0_8px_32px_rgba(0,0,0,0.1)] flex-1 overflow-y-auto" style={{ backdropFilter: 'blur(20px) saturate(180%)' }}>
          <h2 className="text-4xl md:text-5xl font-black text-[#CCFF00] mb-4 uppercase tracking-wider" style={{ fontFamily: "'Archivo Black', sans-serif", textShadow: '0 0 30px rgba(204,255,0,0.4)' }}>
            {title}
          </h2>
          <p className="text-gray-300 mb-8 text-lg whitespace-pre-wrap" style={{ fontFamily: "'Inter', sans-serif" }}>
            {body}
          </p>
          
          {/* Project Strategy Images Grid */}
          <div className="grid grid-cols-2 gap-3 mb-8">
            {projectImages.map((img, idx) => (
              <div key={idx} className="relative group overflow-hidden rounded-2xl bg-[#222] border border-white/10">
                <img 
                  src={img} 
                  alt={`Project Strategy ${idx + 1}`}
                  className="w-full h-auto object-cover transition-transform duration-500 group-hover:scale-105"
                  onError={(e) => {
                    // Fallback if image doesn't load
                    const target = e.target as HTMLImageElement;
                    target.style.display = 'none';
                    const parent = target.parentElement;
                    if (parent) {
                      parent.innerHTML = `<div class="w-full h-48 flex items-center justify-center text-white/50">Image ${idx + 1}</div>`;
                    }
                  }}
                />
              </div>
            ))}
          </div>

          {/* Level Cards */}
          {items && (
            <div className="grid grid-cols-2 gap-6 mt-8">
              {items.map((item, idx) => {
                const gradients = [
                  'from-[rgba(139,69,19,0.6)] to-[rgba(75,0,130,0.6)]', // Howlin' 404
                  'from-[rgba(70,130,180,0.6)] to-[rgba(176,196,222,0.6)]', // NASA
                  'from-[rgba(139,69,19,0.6)] to-[rgba(160,82,45,0.6)]', // Bonnie & Clyde
                  'from-[rgba(25,25,112,0.6)] to-[rgba(70,130,180,0.6)]' // Nocturne 07
                ];
                return (
                  <div key={idx} className="relative group overflow-hidden rounded-2xl bg-white/2 backdrop-blur-[15px] border border-white/8 hover:border-[#CCFF00]/30 transition-all">
                    <div className={`h-48 bg-gradient-to-br ${gradients[idx] || 'from-gray-700 to-gray-900'} flex items-center justify-center`}>
                      <span className="text-2xl font-black text-[#CCFF00] uppercase" style={{ fontFamily: "'Archivo Black', sans-serif" }}>
                        {item}
                      </span>
                    </div>
                    <div className="p-6 bg-[#1a1a1a]">
                      <div className="text-2xl font-black text-[#CCFF00] mb-2 uppercase" style={{ fontFamily: "'Archivo Black', sans-serif" }}>
                        {item}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </SlideContainer>
  );
};

// --- Main App ---

export default function PresentationApp() {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [isFullscreen, setIsFullscreen] = useState(false);

  const totalSlides = slides.length;

  const nextSlide = () => {
    if (currentSlide < totalSlides - 1) setCurrentSlide(prev => prev + 1);
  };

  const prevSlide = () => {
    if (currentSlide > 0) setCurrentSlide(prev => prev - 1);
  };

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen();
      setIsFullscreen(true);
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
        setIsFullscreen(false);
      }
    }
  };

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight' || e.key === 'Space') nextSlide();
      if (e.key === 'ArrowLeft') prevSlide();
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [currentSlide]);

  const renderSlide = (slide: SlideContent) => {
    switch (slide.type) {
      case 'title':
        return <TitleSlide title={slide.title} subtitle={slide.subtitle} />;
      case 'index':
        return <IndexSlide items={slide.items} />;
      case 'quote':
        return <QuoteSlide highlight={slide.highlight} title={slide.title} />;
      case 'image-grid':
        return <ImageGridSlide title={slide.title} body={slide.body} items={slide.items} />;
      case 'profile':
        return <ProfileSlide title={slide.title} subtitle={slide.subtitle} body={slide.body} highlight={slide.highlight} />;
      case 'profile-detail':
        return <ProfileDetailSlide title={slide.title} items={slide.items} links={slide.links} />;
      case 'content':
      default:
        return <ContentSlide 
                  title={slide.title} 
                  subtitle={slide.subtitle}
                  body={slide.body} 
                  highlight={slide.highlight} 
                  items={slide.items}
                  links={slide.links}
               />;
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#050505] font-sans text-white selection:bg-[#CCFF00] selection:text-black" style={{ fontFamily: "'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Noto Sans KR', sans-serif" }}>
      {/* Add Google Fonts */}
      <link rel="preconnect" href="https://fonts.googleapis.com" />
      <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      <link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@300;500;800&family=Noto+Sans+KR:wght@300;500;700;900&display=swap" rel="stylesheet" />
      
      {/* Viewport Frame (Simulating the 16:9 Slide Area) */}
      <div className="w-full max-w-6xl aspect-video bg-[#050505] relative shadow-2xl border border-white/10 overflow-hidden rounded-sm flex flex-col">
        
        {/* Slide Content Area */}
        <div className="flex-1 relative z-10 transition-opacity duration-300">
          {renderSlide(slides[currentSlide])}
        </div>

        {/* Background Effects (Global) */}
        <div className="absolute inset-0 z-0 pointer-events-none">
            {/* Decorative orbs */}
            <div className="absolute top-[10%] left-[8%] w-[360px] h-[360px] rounded-full bg-gradient-radial from-[#CCFF00] to-transparent blur-[80px] opacity-55"></div>
            <div className="absolute bottom-[8%] right-[6%] w-[520px] h-[520px] rounded-full bg-gradient-radial from-[#4b0082] to-transparent blur-[80px] opacity-55"></div>
            <div className="absolute top-[62%] left-[52%] w-[220px] h-[220px] rounded-full bg-gradient-radial from-[#001f3f] to-transparent blur-[80px] opacity-55"></div>
        </div>

        {/* Footer / Progress Bar */}
        <div className="absolute bottom-0 left-0 w-full h-1 bg-gray-900 z-50">
          <div 
            className="h-full bg-[#CCFF00] transition-all duration-300 ease-out"
            style={{ width: `${((currentSlide + 1) / totalSlides) * 100}%` }}
          />
        </div>

        {/* Slide Number */}
        <div className="absolute bottom-4 right-6 text-gray-500 text-sm font-mono z-50">
          {currentSlide + 1} <span className="text-gray-700">/</span> {totalSlides}
        </div>

      </div>

      {/* Controls */}
      <div className="mt-8 flex items-center gap-6">
        <button 
          onClick={prevSlide} 
          disabled={currentSlide === 0}
          className="p-3 rounded-full hover:bg-white/10 disabled:opacity-30 disabled:hover:bg-transparent transition-colors text-[#CCFF00]"
        >
          <ChevronLeft size={32} />
        </button>

        <span className="text-gray-500 font-medium">
          Use Arrow Keys to Navigate
        </span>

        <button 
          onClick={nextSlide} 
          disabled={currentSlide === totalSlides - 1}
          className="p-3 rounded-full hover:bg-white/10 disabled:opacity-30 disabled:hover:bg-transparent transition-colors text-[#CCFF00]"
        >
          <ChevronRight size={32} />
        </button>

        <div className="w-px h-8 bg-white/20 mx-2" />

        <button 
          onClick={toggleFullscreen}
          className="p-3 rounded-full hover:bg-white/10 transition-colors text-gray-400 hover:text-white"
          title="Toggle Fullscreen"
        >
          {isFullscreen ? <Minimize2 size={24} /> : <Maximize2 size={24} />}
        </button>
      </div>

    </div>
  );
}

