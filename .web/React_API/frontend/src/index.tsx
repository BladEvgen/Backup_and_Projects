import React, { useState, useEffect } from "react";
import { createRoot } from "react-dom/client";
import "./css/bootstrap/bootstrap.css";
import "./css/fontawesome/css/all.css";
import "./index.css";
import axios from "axios";
import Router from "./components/router";
import { Interface } from "readline";

interface Question {
  question_id: number;
  question_text: string;
  options: string[];
}

interface Score {
  team_id: number;
  team_name: string;
  score: number;
}
function App() {
  const [question, setQuestion] = useState<Question | null>(null);
  const [scores, setScores] = useState<Score[]>([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const questionResponse = await axios.get(
          "http://localhost:8000/api/question"
        );
        setQuestion(questionResponse.data);

        const scoresResponse = await axios.get(
          "http://localhost:8000/api/scores"
        );
        setScores(scoresResponse.data.scores);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }
    fetchData();
  }, []);

  return (
    <div className="container mt-4 text-white bg-dark">
      {question && (
        <div className="card bg-secondary text-white mb-3">
          <div className="card-header">Вопрос</div>
          <div className="card-body">
            <p className="card-text">Номер вопроса: {question.question_id}</p>
            <p className="card-text">Вопрос: {question.question_text}</p>
            <p className="card-text">Варианты:</p>
            <select className="form-select">
              {question.options.map((option, index) => (
                <option key={index} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </div>
        </div>
      )}

      <hr />

      <div>
        <h2 className="mb-3">Счет</h2>
        <ul className="list-group">
          {scores.map((score, index) => (
            <li key={index} className="list-group-item bg-secondary text-white">
              Номер команды: {score.team_id}, Название: {score.team_name}, Счет:{" "}
              {score.score}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
createRoot(document.getElementById("root")!).render(<Router />);
