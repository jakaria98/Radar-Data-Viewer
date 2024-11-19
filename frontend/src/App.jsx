import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import DataViewer from "./Pages/DataViewer";
import UploadFile from "./Pages/UploadFile";

function App() {
	return (
		<Router>
			<Routes>
				<Route path="/" element={<DataViewer />} />
				<Route path="/upload" element={<UploadFile />} />
			</Routes>
		</Router>
	);
}

export default App;
