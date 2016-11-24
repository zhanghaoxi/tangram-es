#include "util/yamlHelper.h"

#include "log.h"
#include "csscolorparser.hpp"

#define MAP_DELIM '.'
#define SEQ_DELIM '#'

namespace Tangram {

YamlPath::YamlPath() {}

YamlPath::YamlPath(const std::string& path)
    : codedPath(path) {}

YamlPath YamlPath::add(int index) {
    return YamlPath(codedPath + SEQ_DELIM + std::to_string(index));
}

YamlPath YamlPath::add(const std::string& key) {
    if (codedPath.empty()) { return YamlPath(key); }
    return YamlPath(codedPath + MAP_DELIM + key);
}

YAML::Node YamlPath::get(YAML::Node node) {
    size_t pathSize = codedPath.size();
    size_t endToken = 0;

    char delimiter = MAP_DELIM; // First token must be a map key.
    std::string key;

    while (endToken < pathSize) {
        size_t beginToken = endToken;

        while (endToken < pathSize) {
            if (codedPath[endToken] == MAP_DELIM ||
                codedPath[endToken] == SEQ_DELIM) { break; }
            ++endToken;
        }

        // Don't create nodes if key or index do not exist
        const Node& cur = node;
        if (delimiter == MAP_DELIM) {
            key = codedPath.substr(beginToken, endToken - beginToken);
            if (const Node& value = cur[key]) {
                node.reset(value);
            } else {
                // A node in the path was missing, return undefined node.
                return value;
            }
        } else if (delimiter == SEQ_DELIM) {
            int index = std::stoi(&codedPath[beginToken]);
            if (const Node& value = cur[index]) {
                node.reset(value);
            } else {
                return value;
            }
        }

        delimiter = codedPath[endToken]; // Get next character as the delimiter.

        ++endToken; // Move past the delimiter.
    }
    return node;
}

glm::vec4 getColorAsVec4(const Node& node) {
    double val;
    if (getDouble(node, val)) {
        return glm::vec4(val, val, val, 1.0);
    }
    if (node.IsSequence()) {
        return parseVec<glm::vec4>(node);
    }
    if (node.IsScalar()) {
        auto c = CSSColorParser::parse(node.Scalar());
        return glm::vec4(c.r / 255.f, c.g / 255.f, c.b / 255.f, c.a);
    }
    return glm::vec4();
}

std::string parseSequence(const Node& node) {
    std::stringstream sstream;
    for (const auto& val : node) {
        if (!val.IsScalar()) {
            // LOG
            break;
        }

        double value;
        if (getDouble(val, value)) {
            sstream << value << ",";
        } else {
            sstream << val.as<std::string>() << ",";
        }
    }
    return sstream.str();
}

bool getDouble(const Node& node, double& value) {

    if (node.IsScalar()) {
        const std::string& s = node.Scalar().c_str();
        char* pos;;
        value = strtod(s.c_str(), &pos);
        if (pos == s.c_str() + s.length()) {
            return true;
        }
    }

    return false;
}

bool getDouble(const Node& node, double& value, const char* name) {

    if (getDouble(node, value)) { return true; }

    LOGW("Expected a floating point value for '%s' property.:\n%s\n", name, Dump(node).c_str());
    return false;
}

bool getBool(const Node& node, bool& value, const char* name) {
    try {
        value = node.as<bool>();
        return true;
    } catch (const BadConversion& e) {}

    if (name) {
        LOGW("Expected a boolean value for '%s' property.:\n%s\n", name, Dump(node).c_str());
    }
    return false;
}

}
