import React from 'react';

export default function ResultCard({ evaluation }) {
  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-8 max-w-2xl w-full">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Evaluation Results</h2>

      <div className="grid grid-cols-3 gap-4 mb-8">
        <div className="bg-gray-50 p-4 rounded-lg text-center">
          <p className="text-gray-600 font-semibold">Technical Score</p>
          <p className={`text-3xl font-bold ${getScoreColor(evaluation.technical_score)}`}>
            {evaluation.technical_score.toFixed(1)}
          </p>
        </div>

        <div className="bg-gray-50 p-4 rounded-lg text-center">
          <p className="text-gray-600 font-semibold">Communication</p>
          <p className={`text-3xl font-bold ${getScoreColor(evaluation.communication_score)}`}>
            {evaluation.communication_score.toFixed(1)}
          </p>
        </div>

        <div className="bg-gray-50 p-4 rounded-lg text-center">
          <p className="text-gray-600 font-semibold">Confidence</p>
          <p className={`text-3xl font-bold ${getScoreColor(evaluation.confidence_score)}`}>
            {evaluation.confidence_score.toFixed(1)}
          </p>
        </div>
      </div>

      <div className="bg-blue-50 p-4 rounded-lg mb-6">
        <h3 className="font-bold text-gray-800 mb-2">Feedback</h3>
        <p className="text-gray-700">{evaluation.feedback}</p>
      </div>

      <div className="text-center">
        <p className="text-gray-600">Overall Score</p>
        <p className={`text-4xl font-bold ${getScoreColor(evaluation.overall_score)}`}>
          {evaluation.overall_score.toFixed(1)}/100
        </p>
      </div>
    </div>
  );
}
