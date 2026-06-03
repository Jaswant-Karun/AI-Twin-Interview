import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import QuestionCard from '../../components/QuestionCard';
import ResultCard from '../../components/ResultCard';
import { useInterviewStore } from '../../services/interviewStore';
import toast from 'react-hot-toast';

export default function Interview() {
  const router = useRouter();
  const { interviewId } = router.query;
  const {
    interview,
    questions,
    currentQuestionIndex,
    evaluations,
    loading,
    fetchQuestions,
    submitAnswer,
    endInterview
  } = useInterviewStore();

  useEffect(() => {
    if (interviewId) {
      fetchQuestions(interviewId);
    }
  }, [interviewId]);

  const handleAnswerSubmit = async (answer) => {
    try {
      const question = questions[currentQuestionIndex];
      await submitAnswer(interviewId, question.id, answer);
      toast.success('Answer evaluated!');
    } catch (error) {
      toast.error('Failed to evaluate answer');
    }
  };

  const handleFinishInterview = async () => {
    try {
      await endInterview(interviewId);
      toast.success('Interview completed!');
      router.push(`/results/${interviewId}`);
    } catch (error) {
      toast.error('Failed to finish interview');
    }
  };

  if (!questions.length) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <p className="text-xl text-gray-700">Loading questions...</p>
        </div>
      </div>
    );
  }

  const currentQuestion = questions[currentQuestionIndex];
  const currentEvaluation = evaluations[currentQuestionIndex];

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-2xl mx-auto">
        {/* Progress bar */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <h1 className="text-2xl font-bold text-gray-800">Interview Progress</h1>
            <span className="text-gray-600">
              Question {currentQuestionIndex + 1} of {questions.length}
            </span>
          </div>
          <div className="bg-gray-300 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all"
              style={{
                width: `${((currentQuestionIndex + 1) / questions.length) * 100}%`
              }}
            />
          </div>
        </div>

        {/* Question or Result */}
        <div className="flex justify-center mb-8">
          {currentEvaluation ? (
            <ResultCard evaluation={currentEvaluation} />
          ) : (
            <QuestionCard
              question={currentQuestion}
              interviewId={interviewId}
              onAnswerSubmit={handleAnswerSubmit}
              isLoading={loading}
            />
          )}
        </div>

        {/* Navigation */}
        <div className="flex justify-center gap-4">
          {currentQuestionIndex === questions.length - 1 && evaluations.length === questions.length ? (
            <button
              onClick={handleFinishInterview}
              className="px-8 py-3 bg-green-600 text-white rounded-lg font-bold hover:bg-green-700"
            >
              Finish Interview
            </button>
          ) : (
            currentEvaluation && (
              <button
                onClick={() => {
                  // Move to next question
                }}
                className="px-8 py-3 bg-blue-600 text-white rounded-lg font-bold hover:bg-blue-700"
              >
                Next Question
              </button>
            )
          )}
        </div>
      </div>
    </div>
  );
}
