import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class AuthService {
  final String baseUrl = "http://localhost:8000";

  // 🔐 LOGIN REAL CON FASTAPI
  Future<bool> login(String username, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/token'),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: {
          'username': username,
          'password': password,
        },
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final String token = data['access_token'];

        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('jwt_token', token);

        print("✅ TOKEN GUARDADO: $token");

        return true;
      } else {
        print("❌ ERROR LOGIN: ${response.statusCode}");
        print(response.body);
      }
    } catch (e) {
      print("❌ EXCEPCIÓN LOGIN: $e");
    }

    return false;
  }

  // 🔎 OBTENER TOKEN
  Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('jwt_token');
  }

  // 🚪 LOGOUT
  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('jwt_token');
  }
}