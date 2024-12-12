import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import ProtectedRoute from "./Components/ProtectedRoute";
import DataViewer from "./Pages/DataViewer";
import LoginPage from "./Pages/LoginPage";
import RegisterUser from "./Pages/RegisterUser";
import UploadFile from "./Pages/UploadFile";

function App() {
	return (
		<Router>
			<Routes>
				<Route path="/login" element={<LoginPage />} />

				<Route
					path="/addUser"
					element={
						<ProtectedRoute>
							<RegisterUser />
						</ProtectedRoute>
					}
				/>

				<Route
					path="/"
					element={
						<ProtectedRoute>
							<DataViewer />
						</ProtectedRoute>
					}
				/>
				<Route
					path="/upload"
					element={
						<ProtectedRoute>
							<UploadFile />
						</ProtectedRoute>
					}
				/>
			</Routes>
		</Router>
	);
}

export default App;
