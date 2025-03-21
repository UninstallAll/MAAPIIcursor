import React, { useState } from 'react';

const HexagonComponent = () => {
    const [count, setCount] = useState(1); // 新增状态来管理六边形数量

    const handleCountChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setCount(Number(event.target.value)); // 更新六边形数量
    };

    return (
        <div>
            <input 
                type="number" 
                value={count} 
                onChange={handleCountChange} 
                min="1" 
                max="100" 
            />
            <div className="hexagon-container">
                {[...Array(count)].map((_, index) => (
                    <div key={index} className="hexagon" style={{ margin: '10px' }}>
                        {/* 绘制六边形的代码 */}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default HexagonComponent; 