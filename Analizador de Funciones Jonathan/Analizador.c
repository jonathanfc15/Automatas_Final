#include <cctype>
#include <iostream>
#include <string>
#include <vector>

enum class TokenType {
    Identifier,
    Number,
    Text,
    Symbol,
    Invalid
};

struct Token {
    TokenType type;
    std::string lexeme;
    std::size_t position;
};

std::vector<Token> tokenize(const std::string &source) {
    std::vector<Token> tokens;

    for (std::size_t i = 0; i < source.size();) {
        if (std::isspace(static_cast<unsigned char>(source[i]))) {
            ++i;
            continue;
        }

        const std::size_t start = i;
        if (std::isalpha(static_cast<unsigned char>(source[i])) || source[i] == '_') {
            ++i;
            while (i < source.size() &&
                   (std::isalnum(static_cast<unsigned char>(source[i])) || source[i] == '_')) {
                ++i;
            }
            tokens.push_back({TokenType::Identifier, source.substr(start, i - start), start});
        } else if (std::isdigit(static_cast<unsigned char>(source[i]))) {
            ++i;
            while (i < source.size() &&
                   (std::isdigit(static_cast<unsigned char>(source[i])) || source[i] == '.')) {
                ++i;
            }
            tokens.push_back({TokenType::Number, source.substr(start, i - start), start});
        } else if (source[i] == '"' || source[i] == '\'') {
            const char quote = source[i++];
            bool closed = false;
            while (i < source.size()) {
                if (source[i] == '\\' && i + 1 < source.size()) {
                    i += 2;
                } else if (source[i++] == quote) {
                    closed = true;
                    break;
                } else {
                    continue;
                }
            }
            tokens.push_back({
                closed ? TokenType::Text : TokenType::Invalid,
                source.substr(start, i - start), start
            });
        } else {
            const std::string symbols = "(){}[],;=+-*/<>!&|%.";
            if (symbols.find(source[i]) != std::string::npos) {
                tokens.push_back({TokenType::Symbol, std::string(1, source[i]), i});
            } else {
                tokens.push_back({TokenType::Invalid, std::string(1, source[i]), i});
            }
            ++i;
        }
    }

    return tokens;
}

enum class State {
    Start,
    ReturnType,
    FunctionName,
    OpenParameters,
    ParameterType,
    ParameterName,
    Comma,
    OpenBody,
    Body,
    Accept,
    Error
};

const char *stateName(State state) {
    switch (state) {
        case State::Start: return "inicio";
        case State::ReturnType: return "tipo de retorno";
        case State::FunctionName: return "nombre de función";
        case State::OpenParameters: return "paréntesis de parámetros";
        case State::ParameterType: return "tipo de parámetro";
        case State::ParameterName: return "nombre de parámetro";
        case State::Comma: return "separador de parámetros";
        case State::OpenBody: return "apertura del cuerpo";
        case State::Body: return "cuerpo de función";
        case State::Accept: return "aceptación";
        case State::Error: return "error";
    }
    return "desconocido";
}

struct AnalysisResult {
    bool valid;
    std::string message;
};

AnalysisResult analyzeFunction(const std::string &source) {
    const auto tokens = tokenize(source);
    if (tokens.empty()) {
        return {false, "La entrada está vacía."};
    }

    State state = State::Start;
    std::size_t index = 0;
    std::string error;

    auto fail = [&](const std::string &expected, const Token *found) {
        state = State::Error;
        if (found == nullptr) {
            error = "Se esperaba " + expected + " al final de la entrada.";
        } else {
            error = "Se esperaba " + expected + ", pero se encontró \"" +
                    found->lexeme + "\" en la posición " +
                    std::to_string(found->position + 1) + ".";
        }
    };

    while (state != State::Accept && state != State::Error) {
        const Token *token = index < tokens.size() ? &tokens[index] : nullptr;

        switch (state) {
            case State::Start:
                if (token != nullptr && token->type == TokenType::Identifier) {
                    state = State::ReturnType;
                    ++index;
                } else {
                    fail("un tipo de retorno", token);
                }
                break;

            case State::ReturnType:
                if (token != nullptr && token->type == TokenType::Identifier) {
                    state = State::FunctionName;
                    ++index;
                } else {
                    fail("el nombre de la funcion", token);
                }
                break;

            case State::FunctionName:
                if (token != nullptr && token->lexeme == "(") {
                    state = State::OpenParameters;
                    ++index;
                } else {
                    fail("\"(\"", token);
                }
                break;

            case State::OpenParameters:
                if (token != nullptr && token->lexeme == ")") {
                    state = State::OpenBody;
                    ++index;
                } else if (token != nullptr && token->type == TokenType::Identifier) {
                    state = State::ParameterType;
                    ++index;
                } else {
                    fail("un tipo de parametro o \")\"", token);
                }
                break;

            case State::ParameterType:
                if (token != nullptr && token->type == TokenType::Identifier) {
                    state = State::ParameterName;
                    ++index;
                } else if (token != nullptr && token->lexeme == ",") {
                    fail("el nombre del parámetro antes de \",\"", token);
                } else {
                    fail("el nombre del parámetro", token);
                }
                break;

            case State::ParameterName:
                if (token != nullptr && token->lexeme == ",") {
                    state = State::Comma;
                    ++index;
                } else if (token != nullptr && token->lexeme == ")") {
                    state = State::OpenBody;
                    ++index;
                } else {
                    fail("\",\" o \")\"", token);
                }
                break;

            case State::Comma:
                if (token != nullptr && token->type == TokenType::Identifier) {
                    state = State::ParameterType;
                    ++index;
                } else {
                    fail("el tipo del siguiente parámetro", token);
                }
                break;

            case State::OpenBody:
                if (token != nullptr && token->lexeme == "{") {
                    state = State::Body;
                    ++index;
                } else {
                    fail("\"{\"", token);
                }
                break;

            case State::Body:
                if (token == nullptr) {
                    fail("\"}\"", nullptr);
                } else if (token->lexeme == "}") {
                    state = State::Accept;
                    ++index;
                } else if (token->lexeme == "{") {
                    fail("un cuerpo sin llaves anidadas", token);
                } else if (token->type == TokenType::Invalid) {
                    fail("un token válido", token);
                } else {
                    ++index;
                }
                break;

            case State::Accept:
            case State::Error:
                break;
        }
    }

    if (state == State::Accept && index < tokens.size()) {
        return {
            false, "Hay tokens después del cierre de la funcion en la posición " +
                   std::to_string(tokens[index].position + 1) + "."
        };
    }
    if (state == State::Error) {
        return {false, error + " Estado del AFD: " + stateName(state) + "."};
    }
    return {true, "La función pertenece al lenguaje reconocido por el AFD."};
}

int main() {
    std::cout << "Analizador de funciones mediante un Automata Finito Determinista\n";
    std::cout << "Formato: tipo nombre(tipo parametro, ...) { instrucciones }\n";
    std::cout << "Nota: este AFD no permite llaves anidadas dentro del cuerpo.\n";
    std::cout << "Escriba una función (o \"salir\" para terminar):\n\n";

    std::string function;
    while (std::getline(std::cin, function) && function != "salir") {
        const AnalysisResult result = analyzeFunction(function);
        std::cout << (result.valid ? "\n[ACEPTADA] " : "\n[RECHAZADA] ")
                << result.message << "\n\n";
        std::cout << "Escriba otra funcion (o \"salir\" para terminar):\n";
    }

    return 0;
}
