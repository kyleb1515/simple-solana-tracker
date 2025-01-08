function App() {
    const [priceData] = React.useState({
        timestamp: new Date().toLocaleTimeString(),
        sol_amount: 0.28743368,
        sol_price: 196.18,
        pool_value: 56.39
    });

    return (
        <div className="min-h-screen flex items-center justify-center">
            <div className="bg-gray-800 p-8 rounded-lg shadow-lg max-w-md w-full">
                <h1 className="text-3xl font-bold mb-6 text-center">Solana Price Tracker</h1>
                <div className="space-y-4">
                    <div className="bg-gray-700 p-4 rounded">
                        <p className="text-gray-400">Last Updated</p>
                        <p className="text-xl">{priceData.timestamp}</p>
                    </div>
                    <div className="bg-gray-700 p-4 rounded">
                        <p className="text-gray-400">SOL Price</p>
                        <p className="text-xl">${priceData.sol_price.toFixed(2)}</p>
                    </div>
                    <div className="bg-gray-700 p-4 rounded">
                        <p className="text-gray-400">Pool SOL Amount</p>
                        <p className="text-xl">{priceData.sol_amount.toFixed(8)}</p>
                    </div>
                    <div className="bg-gray-700 p-4 rounded">
                        <p className="text-gray-400">Pool Value</p>
                        <p className="text-xl">${priceData.pool_value.toFixed(2)}</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

ReactDOM.render(<App />, document.getElementById('root'));