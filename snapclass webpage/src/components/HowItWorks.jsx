import React from 'react';
import { Download, Camera, Zap, CheckCircle } from 'lucide-react';

const HowItWorks = () => {
  const steps = [
    {
      icon: Download,
      emoji: '📱',
      title: 'Install the App',
      description: 'Download SnapClass from your device\'s app store and complete the quick setup process.',
      details: ['Available on iOS and Android', 'Quick 2-minute setup', 'No account required']
    },
    {
      icon: Camera,
      emoji: '📸',
      title: 'Snap a Photo',
      description: 'Take a clear photo of handwritten notes, textbook pages, or any learning material.',
      details: ['Works with any handwriting', 'Supports multiple languages', 'Auto-focus and crop']
    },
    {
      icon: Zap,
      emoji: '⚡',
      title: 'Get Results Instantly',
      description: 'Receive AI-powered summaries, explanations, and answers within seconds.',
      details: ['Instant processing', 'Detailed explanations', 'Multiple question types']
    },
    {
      icon: CheckCircle,
      emoji: '🚀',
      title: 'Stay Productive',
      description: 'Continue learning and teaching effectively, even without internet connectivity.',
      details: ['Save results offline', 'Share with classmates', 'Build knowledge base']
    }
  ];

  return (
    <section id="how-it-works" className="py-20 bg-gradient-to-br from-white to-purple-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-6">
            How to Use SnapClass
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Get started in minutes and transform your learning experience with just four simple steps
          </p>
        </div>

        {/* Desktop Flow */}
        <div className="hidden lg:block">
          <div className="relative">
            {/* Connection Line */}
            <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-gradient-to-r from-purple-300 via-purple-500 to-purple-300 transform -translate-y-1/2"></div>
            
            <div className="grid grid-cols-4 gap-8">
              {steps.map((step, index) => (
                <div key={index} className="relative">
                  <div className="bg-white rounded-2xl p-6 shadow-lg text-center relative z-10 border border-purple-100">
                    <div className="w-16 h-16 bg-gradient-to-r from-purple-600 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
                      <span className="text-2xl">{step.emoji}</span>
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-3">
                      {step.title}
                    </h3>
                    <p className="text-gray-600 text-sm mb-4">
                      {step.description}
                    </p>
                    <div className="space-y-2">
                      {step.details.map((detail, detailIndex) => (
                        <div key={detailIndex} className="flex items-center justify-center">
                          <div className="w-1.5 h-1.5 bg-purple-600 rounded-full mr-2"></div>
                          <span className="text-xs text-gray-600">{detail}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  {/* Step Number */}
                  <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center font-bold text-sm z-20">
                    {index + 1}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Mobile Flow */}
        <div className="lg:hidden space-y-8">
          {steps.map((step, index) => (
            <div key={index} className="flex items-start">
              <div className="w-12 h-12 bg-gradient-to-r from-purple-600 to-purple-500 rounded-full flex items-center justify-center mr-4 flex-shrink-0">
                <span className="text-white font-bold">{index + 1}</span>
              </div>
              <div className="bg-white rounded-2xl p-6 shadow-lg flex-1 border border-purple-100">
                <div className="flex items-center mb-3">
                  <span className="text-2xl mr-3">{step.emoji}</span>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {step.title}
                  </h3>
                </div>
                <p className="text-gray-600 mb-4">
                  {step.description}
                </p>
                <div className="space-y-2">
                  {step.details.map((detail, detailIndex) => (
                    <div key={detailIndex} className="flex items-center">
                      <div className="w-1.5 h-1.5 bg-purple-600 rounded-full mr-2"></div>
                      <span className="text-sm text-gray-600">{detail}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Call to Action */}
        <div className="text-center mt-16">
          <div className="bg-gradient-to-r from-purple-600 to-purple-500 rounded-3xl p-8 text-white">
            <h3 className="text-2xl font-bold mb-4">Ready to Get Started?</h3>
            <p className="text-purple-100 mb-6 max-w-2xl mx-auto">
              Join thousands of students and teachers who are already using SnapClass to enhance their learning experience.
            </p>
            <button className="bg-white text-purple-600 px-8 py-3 rounded-full font-semibold hover:shadow-lg transform hover:scale-105 transition-all duration-300">
              Download SnapClass Now
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;