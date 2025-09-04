import React from 'react';
import { GraduationCap, UserCheck, School, MapPin } from 'lucide-react';

const Audience = () => {
  const audiences = [
    {
      icon: GraduationCap,
      emoji: '🎓',
      title: 'School Students',
      description: 'To test their understanding, clarify concepts, and receive personalized feedback based on textbook content and teacher explanations — all offline.',
      benefits: ['Offline Self-Evaluation', 'Concept Reinforcement', 'Personalized Reports']
    },
    {
      icon: UserCheck,
      emoji: '👩‍🏫',
      title: 'Teachers',
      description: 'To assess student comprehension, generate automatic quizzes from their own materials, and receive actionable insights into each student’s learning level.',
      benefits: ['Effortless Test Creation', 'Insightful Analytics', 'Time-Saving Tool']
    },
    {
      icon: School,
      emoji: '🏫',
      title: 'School Administrators',
      description: 'To monitor class performance, identify learning gaps across different groups, and improve teaching strategies based on offline test analytics.',
      benefits: ['Class Performance Dashboard', 'Informed Decision Making', 'No Connectivity Dependency']
    },
    {
      icon: MapPin,
      emoji: '🏕️',
      title: 'Remote Education Centers',
      description: 'To bring AI-powered learning and assessment tools into classrooms without internet access, ensuring inclusive education for all learners.',
      benefits: ['Zero Internet Required', 'Inclusive Education Access', 'Simple Infrastructure Needs']
    }
  ];

  return (
    <section id="audience" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-6">
            Who Can Use SnapClass.AI?
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Designed for learners and educators at every level, in every environment
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {audiences.map((audience, index) => (
            <div 
              key={index}
              className="bg-gradient-to-br from-purple-50 to-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-300 border border-purple-100"
            >
              <div className="flex items-start">
                <div className="w-16 h-16 bg-gradient-to-r from-purple-600 to-purple-500 rounded-full flex items-center justify-center mr-6 flex-shrink-0">
                  <span className="text-2xl">{audience.emoji}</span>
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">
                    {audience.title}
                  </h3>
                  <p className="text-gray-600 mb-4 leading-relaxed">
                    {audience.description}
                  </p>
                  <div className="space-y-2">
                    {audience.benefits.map((benefit, benefitIndex) => (
                      <div key={benefitIndex} className="flex items-center">
                        <div className="w-2 h-2 bg-purple-600 rounded-full mr-3"></div>
                        <span className="text-sm text-gray-700">{benefit}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Statistics */}
        <div className="mt-16 bg-gradient-to-r from-purple-600 to-purple-500 rounded-3xl p-8 text-white text-center">
          <h3 className="text-2xl font-bold mb-8">Making Education Accessible Everywhere</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <div className="text-3xl font-bold mb-2">2.9B</div>
              <div className="text-purple-100">People worldwide lack internet access</div>
            </div>
            <div>
              <div className="text-3xl font-bold mb-2">100%</div>
              <div className="text-purple-100">Offline functionality</div>
            </div>
            <div>
              <div className="text-3xl font-bold mb-2">∞</div>
              <div className="text-purple-100">Learning possibilities</div>
            </div>
          </div>
        </div>

        {/* Minimum Requirements */}
        <div className="mt-16">
          <div className="text-center mb-8">
            <h3 className="text-2xl font-bold text-gray-900 mb-3">Minimum Requirements</h3>
            <p className="text-gray-600">Ensure your device meets the baseline specifications for the best experience</p>
          </div>

          <div className="bg-gradient-to-br from-purple-50 to-white rounded-3xl p-8 shadow-lg border border-purple-100">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              <div className="bg-white rounded-2xl p-6 border border-purple-100">
                <div className="text-sm text-purple-600 font-semibold mb-1">Processor</div>
                <div className="text-gray-900 font-medium">Snapdragon X Elite</div>
              </div>
              <div className="bg-white rounded-2xl p-6 border border-purple-100">
                <div className="text-sm text-purple-600 font-semibold mb-1">RAM</div>
                <div className="text-gray-900 font-medium">8 GB</div>
              </div>
              <div className="bg-white rounded-2xl p-6 border border-purple-100">
                <div className="text-sm text-purple-600 font-semibold mb-1">Free Storage</div>
                <div className="text-gray-900 font-medium">8 GB</div>
              </div>
              <div className="bg-white rounded-2xl p-6 border border-purple-100">
                <div className="text-sm text-purple-600 font-semibold mb-1">Graphics</div>
                <div className="text-gray-900 font-medium">Qualcomm Adreno X1-85</div>
              </div>
              <div className="bg-white rounded-2xl p-6 border border-purple-100">
                <div className="text-sm text-purple-600 font-semibold mb-1">Operating System</div>
                <div className="text-gray-900 font-medium">Windows 10 or higher</div>
              </div>
              <div className="bg-white rounded-2xl p-6 border border-purple-100">
                <div className="text-sm text-purple-600 font-semibold mb-1">Device</div>
                <div className="text-gray-900 font-medium">PC</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Audience;