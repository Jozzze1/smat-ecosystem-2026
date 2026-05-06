import 'dart:convert';
import 'package:http/http.dart' as http;

import '../models/estacion.dart';
import 'auth_service.dart';

class ApiService {
  // 🔥 IMPORTANTE: usa localhost para Flutter Web
  final String baseUrl = "http://localhost:8000";

  // 🔹 GET estaciones
  Future<List<Estacion>> fetchEstaciones() async {
    final url = '$baseUrl/estaciones/';
    print("🌐 URL: $url");

    try {
      final response = await http.get(Uri.parse(url));

      print("📡 STATUS: ${response.statusCode}");
      print("📦 BODY: ${response.body}");

      if (response.statusCode == 200) {
        List<dynamic> jsonResponse = json.decode(response.body);

        print("🧠 PARSED: $jsonResponse");

        return jsonResponse
            .map((data) => Estacion.fromJson(data))
            .toList();
      } else {
        throw Exception('Error servidor: ${response.statusCode}');
      }
    } catch (e) {
      print("❌ ERROR FETCH: $e");
      throw Exception('Error de conexión');
    }
  }

  // 🔹 POST estación (con token)
  Future<bool> crearEstacion(String nombre, String ubicacion) async {
    final token = await AuthService().getToken();
    final url = '$baseUrl/estaciones/';

    print("🔐 TOKEN: $token");

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
        body: jsonEncode({
          'nombre': nombre,
          'ubicacion': ubicacion,
        }),
      );

      print("📡 STATUS POST: ${response.statusCode}");
      print("📦 BODY POST: ${response.body}");

      return response.statusCode == 200;
    } catch (e) {
      print("❌ ERROR POST: $e");
      return false;
    }
  }
}