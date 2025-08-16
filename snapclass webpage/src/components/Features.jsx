import React from 'react';
import { Camera, Brain, WifiOff, Users } from 'lucide-react';

const Features = () => {
  const features = [
    {
      icon: Camera,
      emoji: '📸',
      title: 'Instant Transcription',
      description: 'Creates transcripts of multilinguistic audio and book instantly.',
    },
    {
      icon: Brain,
      emoji: '🧠',
      title: 'AI-Powered Quizzes',
      description: 'Teachers can scan or input content, and SnapClass will generate subjective questions instantly without needing the internet.',
    },
    {
      icon: WifiOff,
      emoji: '🚫',
      title: 'Works Offline',
      description: 'Designed for classrooms with limited connectivity, SnapClass performs all AI tasks — from analysis to test generation — fully offline.',
    },
    {
      icon: Users,
      emoji: '🧑‍🏫',
      title: 'Track Student Learning Gaps',
      description: 'SnapClass highlights conceptual weaknesses based on answers and gives actionable insights to both teachers and students.',
    },
  ];

  return (
    <section id="features" className="py-20 bg-gradient-to-br from-purple-50 to-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-6">
            What SnapClass Can Do
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Powerful AI features that transform how you learn and teach, all working seamlessly offline
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div 
              key={index}
              className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transform hover:-translate-y-2 transition-all duration-300 border border-purple-100"
            >
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-to-r from-purple-600 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">{feature.emoji}</span>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* Feature Demo */}
        <div className="mt-16 bg-white rounded-3xl shadow-2xl overflow-hidden">
          <div className="grid grid-cols-1 lg:grid-cols-2">
            <div className="p-8 lg:p-12 flex flex-col justify-center">
              <h3 className="text-2xl font-bold text-gray-900 mb-4">
                See SnapClass in Action
              </h3>
              <p className="text-gray-600 mb-6">
              SnapClass focuses on understanding how well they were learned. By combining 
              automated content generation and offline connectivity, SnapClass gives teachers 
              what really matters — a clear picture of each student’s comprehension.
              </p>
              <div className="space-y-4">
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center mr-3">
                    <span className="text-purple-600 font-bold text-sm">1</span>
                  </div>
                  <span className="text-gray-700">Upload textbook pdf and lecture audio</span>
                </div>
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center mr-3">
                    <span className="text-purple-600 font-bold text-sm">2</span>
                  </div>
                  <span className="text-gray-700">Create english transcript of multilingual 
                    audio and textbook.
                  </span>
                </div>
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center mr-3">
                    <span className="text-purple-600 font-bold text-sm">3</span>
                  </div>
                  <span className="text-gray-700">Generate subjective questions and publish immediately.</span>
                </div>
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center mr-3">
                    <span className="text-purple-600 font-bold text-sm">4</span>
                  </div>
                  <span className="text-gray-700">Evaluate the answers and give a detailed report.</span>
                </div>
              </div>
            </div>
            <div className="bg-gradient-to-br from-purple-100 to-purple-50 p-8 lg:p-12 flex items-center justify-center">
              <div className="bg-white rounded-2xl p-6 shadow-lg max-w-sm w-full">
                <div className="text-center mb-4">
                  <div className="w-12 h-12 bg-purple-600 rounded-full flex items-center justify-center mx-auto mb-3">
                    <Camera className="text-white" size={24} />
                  </div>
                  <h4 className="font-semibold text-gray-900">Upload pdf and audio</h4> 
                </div>
                <div className="bg-gray-100 rounded-lg p-3 mb-4">
                  <div className="text-xs text-gray-500 mb-1">Student Understanding</div>
                  <div className="bg-white rounded p-2 text-sm">
                    "Photosynthesis happens in the chloroplast of plant cells..."
                  </div>
                </div>
                <div className="bg-purple-50 rounded-lg p-3">
                  <div className="text-xs text-purple-600 font-semibold mb-1">AI Insight</div>
                  <div className="text-sm text-gray-700">
                  Student misunderstood the role of chloroplasts. Summary: Photosynthesis converts light energy into chemical energy stored in glucose, and occurs in the chloroplast.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Features;