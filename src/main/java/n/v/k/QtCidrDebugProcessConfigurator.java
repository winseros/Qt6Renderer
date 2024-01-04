package n.v.k;

import com.intellij.ide.plugins.IdeaPluginDescriptor;
import com.intellij.ide.plugins.PluginManagerCore;
import com.intellij.openapi.extensions.PluginId;
import com.jetbrains.cidr.execution.debugger.CidrDebugProcess;
import com.jetbrains.cidr.execution.debugger.CidrDebugProcessConfigurator;
import com.jetbrains.cidr.execution.debugger.backend.gdb.GDBDriver;
import com.jetbrains.cidr.execution.debugger.backend.lldb.LLDBDriver;
import org.jetbrains.annotations.NotNull;

public class QtCidrDebugProcessConfigurator implements CidrDebugProcessConfigurator {
    @Override
    public void configure(@NotNull CidrDebugProcess process) {
        IdeaPluginDescriptor plugin = PluginManagerCore.getPlugin(PluginId.getId("n.v.k.Qt6Renderer"));
        assert plugin != null;

        process.postCommand(debuggerDriver -> {
            if (debuggerDriver instanceof LLDBDriver) {
                LLDBRegistrar.register(plugin, process, (LLDBDriver) debuggerDriver);
            } else if (debuggerDriver instanceof GDBDriver) {
                GDBRegistrar.register(plugin, process, (GDBDriver) debuggerDriver);
            }
        });
    }
}
