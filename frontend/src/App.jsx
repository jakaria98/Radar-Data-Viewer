import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import ProtectedRoute from "./Components/ProtectedRoute";
import AllUsers from "./Pages/AllUsers";
import DataViewer from "./Pages/DataViewer";
import History from "./Pages/History";
import LoginPage from "./Pages/LoginPage";
import RegisterUser from "./Pages/RegisterUser";
import UploadFile from "./Pages/UploadFile";

function App() {
	return (
		<Router>
			<Routes>
				<Route path="/" element={<LoginPage />} />
				<Route path="/login" element={<LoginPage />} />

				<Route
					path="/register"
					element={
						<ProtectedRoute>
							<RegisterUser />
						</ProtectedRoute>
					}
				/>

				<Route
					path="/home"
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
				<Route
					path="/all-users"
					element={
						<ProtectedRoute>
							<AllUsers />
						</ProtectedRoute>
					}
				/>
				<Route
					path="/history"
					element={
						<ProtectedRoute>
							<History />
						</ProtectedRoute>
					}
				/>
			</Routes>
		</Router>
	);
}

export default App;
