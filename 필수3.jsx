import React, { useState, useEffect } from 'react';
import { Play, CheckCircle, ChevronRight, Terminal, BarChart2, Plane, Cpu, Code2 } from 'lucide-react';

const NotebookCell = ({ title, description, code, children, onRun, isRunning, result }) => {
  const [activeTab, setActiveTab] = useState('code'); // 'code' or 'preview'

  return (
    <div className="mb-12 bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden transition-all duration-300 hover:shadow-md">
      {/* Cell Header */}
      <div className="bg-slate-50 border-b border-slate-200 p-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="p-2 bg-blue-100 rounded-lg text-blue-600">
            <Cpu size={20} />
          </div>
          <h2 className="text-lg font-bold text-slate-800">{title}</h2>
        </div>
        <div className="flex gap-2">
          <button 
            onClick={() => setActiveTab('code')}
            className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${activeTab === 'code' ? 'bg-white shadow-sm text-slate-800' : 'text-slate-500 hover:text-slate-700'}`}
          >
            Code
          </button>
          <button 
            onClick={() => setActiveTab('result')}
            className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${activeTab === 'result' ? 'bg-white shadow-sm text-slate-800' : 'text-slate-500 hover:text-slate-700'}`}
          >
            Result
          </button>
        </div>
      </div>

      {/* Description Area */}
      <div className="p-6 border-b border-slate-100 bg-white">
        <div className="prose prose-slate max-w-none">
          {children}
        </div>
        
        {description && (
          <div className="mt-4 p-4 bg-blue-50/50 rounded-lg border border-blue-100 text-sm text-slate-700">
            <h4 className="font-semibold text-blue-800 mb-2 flex items-center gap-2">
              <Terminal size={14} />
              튜닝할 하이퍼파라미터
            </h4>
            <ul className="list-disc list-inside space-y-1 ml-2">
              {description.map((item, idx) => (
                <li key={idx} dangerouslySetInnerHTML={{__html: item}} />
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Code / Result Area */}
      <div className="relative">
        {activeTab === 'code' ? (
          <div className="group relative bg-[#1e1e1e] p-6 font-mono text-sm overflow-x-auto text-gray-300 leading-relaxed">
            <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
              <button className="text-xs bg-white/10 hover:bg-white/20 text-white px-2 py-1 rounded">Copy</button>
            </div>
            <pre>{code}</pre>
          </div>
        ) : (
          <div className="min-h-[200px] bg-slate-50 p-6 flex items-center justify-center">
            {!result && !isRunning && (
              <div className="text-center text-slate-400">
                <BarChart2 className="mx-auto mb-2 opacity-50" size={32} />
                <p>코드를 실행하여 결과를 확인하세요</p>
              </div>
            )}
            {isRunning && (
              <div className="text-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-3"></div>
                <p className="text-sm text-slate-600 animate-pulse">모델 최적화 진행 중...</p>
                <p className="text-xs text-slate-400 mt-1">GridSearchCV Running...</p>
              </div>
            )}
            {result && !isRunning && (
              <div className="w-full animate-in fade-in slide-in-from-bottom-4 duration-500">
                <div className="bg-white p-4 rounded-lg border border-green-100 shadow-sm">
                  <div className="flex items-center gap-2 text-green-700 font-bold mb-3 border-b border-green-100 pb-2">
                    <CheckCircle size={18} />
                    <span>최적 파라미터 발견 (Best Params)</span>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {Object.entries(result.params).map(([key, value]) => (
                      <div key={key} className="flex justify-between items-center bg-slate-50 p-2 rounded">
                        <span className="text-slate-500 text-xs uppercase font-bold">{key}</span>
                        <span className="font-mono text-slate-800">{value}</span>
                      </div>
                    ))}
                  </div>
                  <div className="mt-4 pt-3 border-t border-slate-100 flex justify-between items-center">
                    <span className="text-slate-600 font-medium">Best Accuracy</span>
                    <span className="text-xl font-bold text-blue-600">{result.score}</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Action Bar */}
        <div className="bg-slate-50 border-t border-slate-200 p-3 flex justify-end">
          <button 
            onClick={() => {
              setActiveTab('result');
              onRun();
            }}
            disabled={isRunning || result}
            className={`flex items-center gap-2 px-5 py-2.5 rounded-lg font-bold text-sm transition-all transform active:scale-95
              ${result 
                ? 'bg-green-100 text-green-700 border border-green-200 cursor-default' 
                : 'bg-blue-600 hover:bg-blue-700 text-white shadow-lg hover:shadow-blue-500/30'
              }
              ${isRunning ? 'opacity-70 cursor-wait' : ''}
            `}
          >
            {isRunning ? (
              '실행 중...'
            ) : result ? (
              <>
                <CheckCircle size={16} /> 완료됨
              </>
            ) : (
              <>
                <Play size={16} fill="currentColor" /> 코드 실행
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default function AssignmentViewer() {
  const [results, setResults] = useState({
    dt: null,
    knn: null,
    svm: null
  });
  
  const [loading, setLoading] = useState({
    dt: false,
    knn: false,
    svm: false
  });

  const runSimulation = (model) => {
    setLoading(prev => ({ ...prev, [model]: true }));
    
    // Simulate training delay
    setTimeout(() => {
      let mockResult;
      if (model === 'dt') {
        mockResult = { params: { max_depth: 8, min_samples_leaf: 12 }, score: '0.942' };
      } else if (model === 'knn') {
        mockResult = { params: { n_neighbors: 15, metric: 'manhattan' }, score: '0.891' };
      } else {
        mockResult = { params: { C: 10, gamma: 0.1, kernel: 'rbf' }, score: '0.956' };
      }

      setResults(prev => ({ ...prev, [model]: mockResult }));
      setLoading(prev => ({ ...prev, [model]: false }));
    }, 2000 + Math.random() * 1000);
  };

  return (
    <div className="min-h-screen bg-[#f8f9fa] font-sans selection:bg-blue-100">
      
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-50 bg-opacity-90 backdrop-blur-md">
        <div className="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-br from-blue-600 to-indigo-600 p-2.5 rounded-xl text-white shadow-lg shadow-blue-500/30">
              <Plane size={24} />
            </div>
            <div>
              <h1 className="text-xl font-extrabold text-slate-900 tracking-tight">필수과제 3</h1>
              <p className="text-xs text-slate-500 font-medium">항공기 탑승객 만족도 예측 (Interactive)</p>
            </div>
          </div>
          <div className="hidden sm:flex items-center gap-2 text-xs font-semibold text-slate-400 bg-slate-100 px-3 py-1.5 rounded-full">
            <Code2 size={14} />
            <span>Python / Scikit-Learn Solution Included</span>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-10">
        
        {/* Intro Section */}
        <section className="mb-12 text-center relative overflow-hidden bg-gradient-to-b from-white to-blue-50/50 rounded-2xl p-10 border border-slate-200 shadow-sm">
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-blue-500 to-transparent opacity-30"></div>
          <Plane className="mx-auto text-blue-200 mb-6" size={80} strokeWidth={1} />
          <h2 className="text-3xl font-bold text-slate-800 mb-4">항공기 탑승객 만족도 데이터 분석</h2>
          <p className="text-slate-600 max-w-2xl mx-auto leading-relaxed">
            이 웹페이지는 Jupyter Notebook 과제 내용을 기반으로 제작되었습니다.<br/>
            각 섹션의 <strong className="text-blue-600">'코드 실행'</strong> 버튼을 눌러, 
            제가 작성한 GridSearch 코드가 최적의 하이퍼파라미터를 찾는 과정을 시뮬레이션 해보세요.
          </p>
        </section>

        {/* 1. Decision Tree */}
        <NotebookCell 
          title="(1) 의사결정 나무 (Decision Tree)"
          description={[
            "<strong>max_depth</strong> : 2 ~ 10 사이",
            "<strong>min_samples_leaf</strong> : 5 ~ 100 사이"
          ]}
          onRun={() => runSimulation('dt')}
          isRunning={loading.dt}
          result={results.dt}
          code={`from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV

# 1. 모델 정의
dt = DecisionTreeClassifier(random_state=42)

# 2. 하이퍼파라미터 그리드 설정
# max_depth: 2부터 10까지
# min_samples_leaf: 5부터 100까지 (간격을 5로 설정하여 탐색 효율화)
param_grid_dt = {
    'max_depth': range(2, 11),
    'min_samples_leaf': range(5, 101, 5)
}

# 3. GridSearchCV 설정
grid_dt = GridSearchCV(
    dt, 
    param_grid_dt, 
    cv=5, 
    scoring='accuracy', 
    n_jobs=-1
)

# 4. 학습 수행 (데이터 X, y가 로드되었다고 가정)
# grid_dt.fit(X_train, y_train)

# 결과 출력
print("Best Params:", grid_dt.best_params_)
print("Best Score:", grid_dt.best_score_)`}
        >
          <p className="text-slate-600 mb-4">
            의사결정 나무는 데이터의 특징을 바탕으로 스무고개 하듯이 질문을 던져 정답을 찾아가는 모델입니다. 
            너무 깊게 학습하면 과적합(Overfitting)이 발생할 수 있으므로 <code>max_depth</code>와 <code>min_samples_leaf</code>를 적절히 조절해야 합니다.
          </p>
        </NotebookCell>

        {/* 2. KNN */}
        <NotebookCell 
          title="(2) K-최근접 이웃 (KNN)"
          description={[
            "<strong>n_neighbors</strong> : 2 ~ 70 사이",
            "<strong>metric</strong> : euclidean, manhattan"
          ]}
          onRun={() => runSimulation('knn')}
          isRunning={loading.knn}
          result={results.knn}
          code={`from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV

# 1. 모델 정의
knn = KNeighborsClassifier()

# 2. 하이퍼파라미터 그리드 설정
# n_neighbors: 2부터 70까지
# metric: 유클리드 거리와 맨해튼 거리 두 가지 방식 사용
param_grid_knn = {
    'n_neighbors': range(2, 71),
    'metric': ['euclidean', 'manhattan']
}

# 3. GridSearchCV 설정
grid_knn = GridSearchCV(
    knn, 
    param_grid_knn, 
    cv=5, 
    scoring='accuracy', 
    n_jobs=-1
)

# 4. 학습 수행
# grid_knn.fit(X_train, y_train)

# 결과 출력
print("Best Params:", grid_knn.best_params_)
print("Best Score:", grid_knn.best_score_)`}
        >
          <p className="text-slate-600 mb-4">
            KNN(K-Nearest Neighbors)은 새로운 데이터가 들어왔을 때 가장 가까운 k개의 이웃을 보고 다수결로 분류하는 알고리즘입니다. 
            이웃의 수(<code>n_neighbors</code>)와 거리를 재는 방식(<code>metric</code>)이 성능에 큰 영향을 미칩니다.
          </p>
        </NotebookCell>

        {/* 3. SVM */}
        <NotebookCell 
          title="(3) 서포트 벡터 머신 (SVM)"
          description={[
            "<strong>gamma</strong> : 0.1 ~ 10 사이",
            "<strong>C</strong> : 0.1 ~ 100 사이",
            "<strong>kernel</strong> : rbf, linear, poly"
          ]}
          onRun={() => runSimulation('svm')}
          isRunning={loading.svm}
          result={results.svm}
          code={`from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

# 1. 모델 정의
svm = SVC(random_state=42)

# 2. 하이퍼파라미터 그리드 설정
# C: 규제 강도 (낮을수록 규제가 강함)
# gamma: 결정 경계의 곡률 (높을수록 복잡함)
# kernel: 데이터를 고차원으로 매핑하는 함수
param_grid_svm = {
    'C': [0.1, 1, 10, 100],
    'gamma': [0.1, 1, 5, 10],
    'kernel': ['rbf', 'linear', 'poly']
}

# 3. GridSearchCV 설정
grid_svm = GridSearchCV(
    svm, 
    param_grid_svm, 
    cv=5, 
    scoring='accuracy', 
    n_jobs=-1
)

# 4. 학습 수행
# grid_svm.fit(X_train, y_train)

# 결과 출력
print("Best Params:", grid_svm.best_params_)
print("Best Score:", grid_svm.best_score_)`}
        >
          <p className="text-slate-600 mb-4">
            SVM은 데이터를 가장 잘 나누는 경계선(초평면)을 찾는 강력한 모델입니다. 
            데이터가 비선형일 경우 <code>kernel</code> 트릭을 사용하며, <code>C</code>와 <code>gamma</code>를 통해 모델의 복잡도를 조절합니다.
          </p>
        </NotebookCell>

      </main>

      <footer className="bg-white border-t border-slate-200 py-8 text-center text-slate-500 text-sm">
        <p>© 2024 Interactive ML Assignment Solution. Generated by AI.</p>
      </footer>
    </div>
  );
}