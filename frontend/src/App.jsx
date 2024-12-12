import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import DataViewer from "./Pages/DataViewer";
import LoginPage from "./Pages/LoginPage";
import RegisterUser from "./Pages/RegisterUser";
import UploadFile from "./Pages/UploadFile";

function App() {
	return (
		<Router>
			<Routes>
				<Route path="/" element={<DataViewer />} />
				<Route path="/upload" element={<UploadFile />} />
				<Route path="/login" element={<LoginPage />} />
				<Route path="/addUser" element={<RegisterUser />} />
			</Routes>
		</Router>
	);
}

export default App;
