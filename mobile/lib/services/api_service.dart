import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/estacion.dart';
import 'auth_service.dart'; // 👈 IMPORTANTE

class ApiService {
  final String baseUrl = "http://192.168.121.46:8000";

  // 🔹 GET (ya lo tenías)
  Future<List<Estacion>> fetchEstaciones() async {
    final response = await http.get(
      Uri.parse('$baseUrl/estaciones/'),
    );

    if (response.statusCode == 200) {
      List jsonResponse = json.decode(response.body);

      return jsonResponse
          .map((data) => Estacion.fromJson(data))
          .toList();
    } else {
      throw Exception('Error al conectar con el servidor SMAT');
    }
  }

  // NUEVO: POST protegido
  Future<bool> crearEstacion(String nombre, String ubicacion) async {
    final token = await AuthService().getToken();

    final response = await http.post(
      Uri.parse('$baseUrl/estaciones/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode({
        'nombre': nombre,
        'ubicacion': ubicacion,
      }),
    );

    return response.statusCode == 200;
  }
}